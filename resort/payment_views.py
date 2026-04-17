"""
Payment views for Demo Beach Resort.
Handles: payment method selection, PayMongo redirect,
         success/cancel pages, and webhooks from PayMongo.
"""
import json
import logging
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.conf import settings
from django.utils import timezone

from .models import Booking, Payment
from .payment_service import (
    initiate_payment, get_payment_service,
    PaymentError, PayMongoService,
)
from .emails import (
    send_booking_confirmation_to_guest,
    send_new_booking_alert_to_admin,
    send_booking_status_update_to_guest,
)

logger = logging.getLogger(__name__)


# ── STEP 3: Payment Method Selection ─────────────────────────────────────────

def payment_checkout(request, booking_reference):
    """
    Payment method selection page.
    Shown after Step 2 (guest details) is submitted.
    Guest chooses: GCash / Maya / GrabPay / Card (all via PayMongo)
    """
    booking = get_object_or_404(Booking, booking_reference=booking_reference)

    # Prevent double payment
    if hasattr(booking, 'payment') and booking.payment.is_paid:
        return redirect('payment_success', booking_reference=booking_reference)

    # Check session ownership
    if request.session.get('booking_reference') != booking_reference:
        return redirect('homepage')

    paymongo_enabled = bool(getattr(settings, 'PAYMONGO_SECRET_KEY', ''))

    context = {
        'booking': booking,
        'paymongo_enabled': paymongo_enabled,
        'step': 3,
        'page': 'booking',
    }
    return render(request, 'resort/payment_checkout.html', context)


# ── Initiate PayMongo Payment ─────────────────────────────────────────────────

def payment_initiate_paymongo(request, booking_reference):
    """
    Creates a PayMongo payment link and redirects guest to PayMongo's
    hosted checkout page where they choose GCash / Maya / Card / GrabPay.
    """
    booking = get_object_or_404(Booking, booking_reference=booking_reference)

    if request.session.get('booking_reference') != booking_reference:
        return redirect('homepage')

    try:
        result = initiate_payment(booking, 'paymongo', request)
        return redirect(result['redirect_url'])
    except PaymentError as e:
        logger.error(f'PayMongo initiation failed for {booking_reference}: {e}')
        messages.error(request, 'Payment initiation failed. Please try again or contact us.')
        return redirect('payment_checkout', booking_reference=booking_reference)


# ── Payment Success Page ──────────────────────────────────────────────────────

def payment_success(request, booking_reference):
    """
    Payment success page — shown after successful payment.
    Also handles PayMongo redirect back to our site.
    """
    booking = get_object_or_404(Booking, booking_reference=booking_reference)

    # If payment came from PayMongo redirect, verify the link status
    if hasattr(booking, 'payment') and booking.payment.provider == 'paymongo':
        link_id = booking.payment.provider_link_id
        if link_id and booking.payment.status != 'paid':
            try:
                paymongo = PayMongoService()
                link_attrs = paymongo.retrieve_payment_link(link_id)
                if link_attrs.get('status') == 'paid':
                    booking.payment.status = 'paid'
                    booking.payment.paid_at = timezone.now()
                    booking.payment.save()
                    booking.status = 'confirmed'
                    booking.save()
                    # Send confirmation emails
                    send_booking_status_update_to_guest(booking)
                    send_new_booking_alert_to_admin(booking)
            except Exception as e:
                logger.error(f'PayMongo link verification error: {e}')

    context = {
        'booking': booking,
        'payment': getattr(booking, 'payment', None),
        'step': 4,
        'page': 'booking',
    }
    return render(request, 'resort/payment_success.html', context)


# ── Payment Cancel / Failure Page ─────────────────────────────────────────────

def payment_cancel(request, booking_reference):
    """Shown when guest cancels or payment fails"""
    booking = get_object_or_404(Booking, booking_reference=booking_reference)
    context = {
        'booking': booking,
        'page': 'booking',
    }
    return render(request, 'resort/payment_cancel.html', context)


# ══════════════════════════════════════════════════════════
#  WEBHOOKS
# ══════════════════════════════════════════════════════════

@csrf_exempt
@require_POST
def webhook_paymongo(request):
    """
    Receives and processes PayMongo webhook events.
    Configure webhook URL in PayMongo dashboard:
    https://dashboard.paymongo.com/developers → Webhooks
    URL: https://yourdomain.com/webhooks/paymongo/
    Events to listen: payment.paid, payment.failed
    """
    payload = request.body
    signature = request.headers.get('Paymongo-Signature', '')

    paymongo = PayMongoService()

    # Verify webhook signature
    if paymongo.webhook_secret and not paymongo.verify_webhook(payload, signature):
        logger.warning('PayMongo webhook signature verification failed')
        return HttpResponse('Invalid signature', status=400)

    try:
        event = json.loads(payload)
        event_type = event.get('data', {}).get('attributes', {}).get('type', '')
        event_data = event.get('data', {}).get('attributes', {})

        logger.info(f'PayMongo webhook received: {event_type}')

        booking, status = paymongo.process_webhook_event(event_type, event_data)

        if status == 'paid':
            send_booking_status_update_to_guest(booking)
            logger.info(f'Booking {booking.booking_reference} marked as paid via PayMongo webhook')
        elif status == 'failed':
            logger.info(f'Payment failed for booking {booking.booking_reference}')

        return HttpResponse('OK', status=200)

    except PaymentError as e:
        logger.error(f'PayMongo webhook processing error: {e}')
        return HttpResponse('Processing error', status=422)
    except Exception as e:
        logger.error(f'PayMongo webhook unexpected error: {e}')
        return HttpResponse('Server error', status=500)
