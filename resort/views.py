import json
from datetime import date, timedelta
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

from .models import VillaType, Villa, Booking, ContactMessage, Testimonial
from .forms import BookingForm, ContactForm
from .emails import (
    send_booking_confirmation_to_guest,
    send_new_booking_alert_to_admin,
    send_contact_autoreply_to_guest,
    send_contact_alert_to_admin,
)


def homepage(request):
    """Main landing page"""
    featured_villas = VillaType.objects.filter(is_featured=True, is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_featured=True)[:4]
    context = {
        'featured_villas': featured_villas,
        'testimonials': testimonials,
        'page': 'home',
    }
    return render(request, 'resort/home.html', context)


def accommodations(request):
    """Accommodations listing page"""
    category = request.GET.get('category', '')
    villas = VillaType.objects.filter(is_active=True)
    if category:
        villas = villas.filter(category=category)
    categories = VillaType.CATEGORY_CHOICES
    context = {
        'villas': villas,
        'categories': categories,
        'active_category': category,
        'page': 'accommodations',
    }
    return render(request, 'resort/accommodations.html', context)


def villa_detail(request, slug):
    """Single villa detail page"""
    villa_type = get_object_or_404(VillaType, slug=slug, is_active=True)
    related = VillaType.objects.filter(is_active=True).exclude(slug=slug)[:3]
    context = {
        'villa': villa_type,
        'related': related,
        'page': 'accommodations',
    }
    return render(request, 'resort/villa_detail.html', context)


def find_accommodation(request):
    """Availability calendar search page"""
    check_in_str = request.GET.get('check_in', '')
    check_out_str = request.GET.get('check_out', '')
    guests = int(request.GET.get('guests', 2))
    available_villas = []
    search_performed = False

    if check_in_str and check_out_str:
        try:
            check_in = date.fromisoformat(check_in_str)
            check_out = date.fromisoformat(check_out_str)
            search_performed = True

            if check_in >= check_out:
                messages.error(request, 'Check-out must be after check-in.')
            elif check_in < date.today():
                messages.error(request, 'Check-in date cannot be in the past.')
            else:
                nights = (check_out - check_in).days
                villa_types = VillaType.objects.filter(is_active=True, max_guests__gte=guests)
                for vt in villa_types:
                    # check if any unit of this type is free
                    for villa in vt.villas.filter(is_active=True):
                        if villa.is_available(check_in, check_out):
                            available_villas.append({
                                'villa_type': vt,
                                'villa': villa,
                                'nights': nights,
                                'total': vt.price_per_night * nights,
                            })
                            break  # one available unit per type is enough for display

        except ValueError:
            messages.error(request, 'Invalid date format.')

    context = {
        'check_in': check_in_str,
        'check_out': check_out_str,
        'guests': guests,
        'available_villas': available_villas,
        'search_performed': search_performed,
        'today': date.today().isoformat(),
        'page': 'find',
    }
    return render(request, 'resort/find_accommodation.html', context)


def booking_step1(request):
    """Booking Step 1 — Select room & dates"""
    # Pre-populate if coming from availability search
    villa_type_id = request.GET.get('villa_type') or request.session.get('booking_villa_type')
    check_in = request.GET.get('check_in') or request.session.get('booking_check_in', '')
    check_out = request.GET.get('check_out') or request.session.get('booking_check_out', '')
    guests = request.GET.get('guests') or request.session.get('booking_guests', 2)

    villa_types = VillaType.objects.filter(is_active=True)
    selected_villa = None
    if villa_type_id:
        try:
            selected_villa = VillaType.objects.get(id=villa_type_id, is_active=True)
        except VillaType.DoesNotExist:
            pass

    if request.method == 'POST':
        villa_type_id = request.POST.get('villa_type_id')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guests = request.POST.get('guests', 2)
        request.session['booking_villa_type'] = villa_type_id
        request.session['booking_check_in'] = check_in
        request.session['booking_check_out'] = check_out
        request.session['booking_guests'] = guests
        return redirect('booking_step2')

    context = {
        'villa_types': villa_types,
        'selected_villa': selected_villa,
        'check_in': check_in,
        'check_out': check_out,
        'guests': guests,
        'today': date.today().isoformat(),
        'step': 1,
        'page': 'booking',
    }
    return render(request, 'resort/booking_step1.html', context)


def booking_step2(request):
    """Booking Step 2 — Guest details form"""
    villa_type_id = request.session.get('booking_villa_type')
    check_in_str = request.session.get('booking_check_in')
    check_out_str = request.session.get('booking_check_out')
    guests = request.session.get('booking_guests', 2)

    if not all([villa_type_id, check_in_str, check_out_str]):
        return redirect('booking_step1')

    try:
        check_in = date.fromisoformat(check_in_str)
        check_out = date.fromisoformat(check_out_str)
        villa_type = get_object_or_404(VillaType, id=villa_type_id, is_active=True)
        nights = (check_out - check_in).days
        total_price = villa_type.price_per_night * nights
    except (ValueError, TypeError):
        return redirect('booking_step1')

    form = BookingForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Find available villa unit
        available_villa = None
        for villa in villa_type.villas.filter(is_active=True):
            if villa.is_available(check_in, check_out):
                available_villa = villa
                break

        if not available_villa:
            messages.error(request, 'Sorry, no units are available for the selected dates.')
            return redirect('booking_step1')

        booking = Booking(
            villa=available_villa,
            guest_first_name=form.cleaned_data['first_name'],
            guest_last_name=form.cleaned_data['last_name'],
            guest_email=form.cleaned_data['email'],
            guest_phone=form.cleaned_data['phone'],
            guest_country=form.cleaned_data.get('country', ''),
            check_in=check_in,
            check_out=check_out,
            adults=form.cleaned_data.get('adults', 2),
            children=form.cleaned_data.get('children', 0),
            special_requests=form.cleaned_data.get('special_requests', ''),
            total_price=total_price,
            nights=nights,
        )
        booking.save()
        request.session['booking_reference'] = booking.booking_reference

        # ── Send initial booking notification emails ───────────────────
        send_booking_confirmation_to_guest(booking)
        send_new_booking_alert_to_admin(booking)

        # Clear session booking data
        for key in ['booking_villa_type', 'booking_check_in', 'booking_check_out', 'booking_guests']:
            request.session.pop(key, None)

        # ── Redirect to payment page ───────────────────────────────────
        return redirect('payment_checkout', booking_reference=booking.booking_reference)

    context = {
        'form': form,
        'villa_type': villa_type,
        'check_in': check_in,
        'check_out': check_out,
        'nights': nights,
        'total_price': total_price,
        'guests': guests,
        'step': 2,
        'page': 'booking',
    }
    return render(request, 'resort/booking_step2.html', context)


def booking_confirmation(request):
    """Booking Step 3 — Confirmation page"""
    booking_reference = request.session.get('booking_reference')
    if not booking_reference:
        return redirect('homepage')
    booking = get_object_or_404(Booking, booking_reference=booking_reference)
    context = {
        'booking': booking,
        'step': 3,
        'page': 'booking',
    }
    return render(request, 'resort/booking_confirmation.html', context)


def contact(request):
    """Contact & Location page"""
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        msg = ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            phone=form.cleaned_data.get('phone', ''),
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message'],
        )
        # ── Send email notifications ──────────────────────────────────
        send_contact_autoreply_to_guest(msg)
        send_contact_alert_to_admin(msg)

        messages.success(request, "Thank you! We'll be in touch shortly.")
        return redirect('contact')
    context = {
        'form': form,
        'page': 'contact',
    }
    return render(request, 'resort/contact.html', context)


def terms_conditions(request):
    return render(request, 'resort/terms.html', {'page': 'terms'})


def booking_policy(request):
    return render(request, 'resort/booking_policy.html', {'page': 'policy'})


# ──── AJAX API ENDPOINTS ──────────────────────────────────────────────────────

@require_GET
def api_check_availability(request):
    """JSON endpoint for calendar availability checks"""
    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')
    villa_type_id = request.GET.get('villa_type_id')

    if not all([check_in_str, check_out_str]):
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        check_in = date.fromisoformat(check_in_str)
        check_out = date.fromisoformat(check_out_str)
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    result = {'available': False, 'villa_types': []}

    qs = VillaType.objects.filter(is_active=True)
    if villa_type_id:
        qs = qs.filter(id=villa_type_id)

    for vt in qs:
        available_unit = None
        for villa in vt.villas.filter(is_active=True):
            if villa.is_available(check_in, check_out):
                available_unit = villa
                break
        if available_unit:
            result['available'] = True
            nights = (check_out - check_in).days
            result['villa_types'].append({
                'id': vt.id,
                'name': vt.name,
                'slug': vt.slug,
                'price_per_night': str(vt.price_per_night),
                'total_price': str(vt.price_per_night * nights),
                'nights': nights,
            })

    return JsonResponse(result)


@require_GET
def api_booked_dates(request):
    """Return list of fully-booked date ranges for a villa type"""
    villa_type_id = request.GET.get('villa_type_id')
    if not villa_type_id:
        return JsonResponse({'error': 'Missing villa_type_id'}, status=400)

    bookings = Booking.objects.filter(
        villa__villa_type_id=villa_type_id,
        status__in=['confirmed', 'pending'],
        check_out__gte=date.today(),
    ).values('check_in', 'check_out')

    ranges = [
        {'start': b['check_in'].isoformat(), 'end': b['check_out'].isoformat()}
        for b in bookings
    ]
    return JsonResponse({'booked_ranges': ranges})


@require_GET  
def api_price_estimate(request):
    """Calculate price estimate for a booking"""
    villa_type_id = request.GET.get('villa_type_id')
    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')

    try:
        vt = VillaType.objects.get(id=villa_type_id, is_active=True)
        check_in = date.fromisoformat(check_in_str)
        check_out = date.fromisoformat(check_out_str)
        nights = (check_out - check_in).days
        if nights < 1:
            raise ValueError('Invalid dates')
        total = vt.price_per_night * nights
        return JsonResponse({
            'nights': nights,
            'price_per_night': str(vt.price_per_night),
            'total': str(total),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
