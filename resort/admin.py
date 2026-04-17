from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages as django_messages
from .models import VillaType, Villa, Booking, ContactMessage, Testimonial, Payment
from .emails import send_booking_status_update_to_guest


@admin.register(VillaType)
class VillaTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_per_night', 'max_guests', 'is_featured', 'is_active', 'sort_order']
    list_editable = ['price_per_night', 'is_featured', 'is_active', 'sort_order']
    list_filter = ['category', 'is_featured', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


class VillaInline(admin.TabularInline):
    model = Villa
    extra = 1


@admin.register(Villa)
class VillaAdmin(admin.ModelAdmin):
    list_display = ['unit_number', 'villa_type', 'floor', 'is_active']
    list_filter = ['villa_type', 'is_active']
    search_fields = ['unit_number']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_reference', 'guest_full_name', 'villa',
        'check_in', 'check_out', 'nights', 'total_price', 'status', 'created_at'
    ]
    list_filter = ['status', 'check_in', 'villa__villa_type']
    search_fields = ['booking_reference', 'guest_first_name', 'guest_last_name', 'guest_email']
    readonly_fields = ['booking_reference', 'created_at', 'updated_at']
    list_editable = ['status']
    date_hierarchy = 'check_in'

    fieldsets = (
        ('Booking Reference', {
            'fields': ('booking_reference', 'status', 'villa')
        }),
        ('Guest Information', {
            'fields': ('guest_first_name', 'guest_last_name', 'guest_email',
                       'guest_phone', 'guest_country')
        }),
        ('Stay Details', {
            'fields': ('check_in', 'check_out', 'nights', 'adults', 'children',
                       'total_price', 'special_requests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Send email to guest when status changes to confirmed or cancelled."""
        if change and 'status' in form.changed_data:
            super().save_model(request, obj, form, change)
            if obj.status in ['confirmed', 'cancelled']:
                sent = send_booking_status_update_to_guest(obj)
                if sent:
                    self.message_user(
                        request,
                        f"✅ Status update email sent to {obj.guest_email}.",
                        django_messages.SUCCESS
                    )
                else:
                    self.message_user(
                        request,
                        f"⚠️ Status saved but email to {obj.guest_email} failed. Check logs.",
                        django_messages.WARNING
                    )
        else:
            super().save_model(request, obj, form, change)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'guest_country', 'rating', 'villa_type', 'is_featured', 'created_at']
    list_editable = ['is_featured']
    list_filter = ['rating', 'is_featured', 'villa_type']
    search_fields = ['guest_name', 'text']


# Customize admin site header
admin.site.site_header = "Demo Beach Resort — Admin"
admin.site.site_title = "Resort Admin"
admin.site.index_title = "Resort Management Dashboard"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'booking_ref', 'guest_name', 'provider', 'method',
        'amount', 'amount_paid', 'status', 'paid_at', 'created_at'
    ]
    list_filter = ['status', 'provider', 'method', 'created_at']
    search_fields = ['booking__booking_reference', 'booking__guest_email',
                     'provider_payment_id', 'provider_link_id']
    readonly_fields = [
        'booking', 'created_at', 'updated_at', 'paid_at',
        'provider_payment_id', 'provider_link_id', 'provider_intent_id',
        'checkout_url', 'webhook_data',
    ]
    date_hierarchy = 'created_at'

    def booking_ref(self, obj):
        return obj.booking.booking_reference
    booking_ref.short_description = 'Booking Ref'

    def guest_name(self, obj):
        return obj.booking.guest_full_name
    guest_name.short_description = 'Guest'


