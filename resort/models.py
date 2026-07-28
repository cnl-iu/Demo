from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class VillaType(models.Model):
    """Represents a category/type of villa accommodation"""
    CATEGORY_CHOICES = [
        ('beachfront', 'Beachfront'),
        ('garden', 'Garden View'),
        ('pool', 'Pool Access'),
        ('cliff', 'Cliffside'),
        ('overwater', 'Overwater'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='beachfront')
    description = models.TextField()
    short_description = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField(default=2)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    size_sqm = models.PositiveIntegerField(help_text='Size in square meters')
    image = models.ImageField(upload_to='villas/', blank=True, null=True)
    image_gallery = models.JSONField(default=list, blank=True)
    amenities = models.JSONField(default=list, help_text='List of amenity strings')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Villa Type'
        verbose_name_plural = 'Villa Types'

    def __str__(self):
        return self.name


class Villa(models.Model):
    """Individual villa unit"""
    villa_type = models.ForeignKey(VillaType, on_delete=models.CASCADE, related_name='villas')
    unit_number = models.CharField(max_length=20)
    floor = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['unit_number']
        unique_together = ['villa_type', 'unit_number']

    def __str__(self):
        return f'{self.villa_type.name} - Unit {self.unit_number}'

    def is_available(self, check_in, check_out):
        """Check if villa is available for given dates"""
        overlapping = self.bookings.filter(
            status__in=['confirmed', 'pending'],
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()
        return not overlapping


class Booking(models.Model):
    """Guest booking record"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    booking_reference = models.CharField(max_length=20, unique=True)
    villa = models.ForeignKey(Villa, on_delete=models.PROTECT, related_name='bookings')
    guest_first_name = models.CharField(max_length=100)
    guest_last_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    guest_country = models.CharField(max_length=100, blank=True)
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1)])
    children = models.PositiveIntegerField(default=0)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    nights = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.booking_reference} — {self.guest_first_name} {self.guest_last_name}'

    @property
    def guest_full_name(self):
        return f'{self.guest_first_name} {self.guest_last_name}'

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import random, string
            self.booking_reference = 'DEMO' + ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=7)
            )
        if not self.nights:
            delta = self.check_out - self.check_in
            self.nights = delta.days
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject}'


class Testimonial(models.Model):
    """Guest testimonials"""
    guest_name = models.CharField(max_length=100)
    guest_country = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=5
    )
    text = models.TextField()
    villa_type = models.ForeignKey(
        VillaType, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials'
    )
    is_featured = models.BooleanField(default=False)
    date_of_stay = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.guest_name} — {self.rating}★'


class Payment(models.Model):
    """Payment record linked to a booking"""

    PROVIDER_CHOICES = [
        ('paymongo', 'PayMongo'),
        ('manual', 'Manual / Bank Transfer'),
    ]
    METHOD_CHOICES = [
        ('gcash', 'GCash'),
        ('maya', 'Maya'),
        ('card', 'Credit / Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('grab_pay', 'GrabPay'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('awaiting_payment', 'Awaiting Payment'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    ]

    booking        = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    provider       = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='paymongo')
    method         = models.CharField(max_length=30, choices=METHOD_CHOICES, blank=True)
    status         = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')

    # Amount fields
    amount         = models.DecimalField(max_digits=12, decimal_places=2)  # PHP
    amount_paid    = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency       = models.CharField(max_length=5, default='PHP')

    # Provider-specific IDs
    provider_payment_id    = models.CharField(max_length=200, blank=True)  # PayMongo payment ID
    provider_link_id       = models.CharField(max_length=200, blank=True)  # PayMongo payment link ID
    provider_intent_id     = models.CharField(max_length=200, blank=True)  # Reserved for future use
    checkout_url           = models.URLField(blank=True)                   # Redirect URL for guest

    # Webhook / raw payload
    webhook_data   = models.JSONField(default=dict, blank=True)

    # Timestamps
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    paid_at        = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f'{self.booking.booking_reference} — {self.get_status_display()} — ₱{self.amount:,.0f}'

    @property
    def is_paid(self):
        return self.status == 'paid'

    @property
    def amount_in_centavos(self):
        """PayMongo requires amounts in centavos (1 PHP = 100 centavos)"""
        return int(self.amount * 100)
