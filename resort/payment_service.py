"""
Payment Service — Demo Beach Resort
Supports: PayMongo (GCash, Maya, Card, GrabPay)

PayMongo Docs: https://developers.paymongo.com
"""
import hmac
import hashlib
import json
import logging
import urllib.request
import urllib.parse
import urllib.error
import base64
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════
#  PAYMONGO SERVICE
# ══════════════════════════════════════════════════════════

class PayMongoService:
    """
    Handles PayMongo payment link creation and webhook verification.
    Supports: GCash, Maya, Card, GrabPay
    """
    BASE_URL = 'https://api.paymongo.com/v1'

    def __init__(self):
        self.secret_key = getattr(settings, 'PAYMONGO_SECRET_KEY', '')
        self.public_key = getattr(settings, 'PAYMONGO_PUBLIC_KEY', '')
        self.webhook_secret = getattr(settings, 'PAYMONGO_WEBHOOK_SECRET', '')

    def _get_auth_header(self):
        """Base64 encode secret key for Authorization header"""
        encoded = base64.b64encode(f'{self.secret_key}:'.encode()).decode()
        return f'Basic {encoded}'

    def _request(self, method, endpoint, data=None):
        """Make authenticated request to PayMongo API"""
        url = f'{self.BASE_URL}{endpoint}'
        headers = {
            'Authorization': self._get_auth_header(),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            logger.error(f'PayMongo API error {e.code}: {error_body}')
            raise PaymentError(f'PayMongo error: {e.code} — {error_body}')

    def create_payment_link(self, booking, request):
        """
        Create a PayMongo payment link for the booking.
        Guest is redirected to this link to choose payment method (GCash, Maya, Card, GrabPay).
        """
        success_url = request.build_absolute_uri(
            reverse('payment_success', args=[booking.booking_reference])
        )
        cancel_url = request.build_absolute_uri(
            reverse('payment_cancel', args=[booking.booking_reference])
        )

        payload = {
            'data': {
                'attributes': {
                    'amount': booking.payment.amount_in_centavos,
                    'currency': 'PHP',
                    'description': (
                        f"Demo Beach Resort — {booking.villa.villa_type.name} "
                        f"({booking.check_in} to {booking.check_out})"
                    ),
                    'remarks': booking.booking_reference,
                    'redirect': {
                        'success': success_url,
                        'failed': cancel_url,
                    },
                    'metadata': {
                        'booking_reference': booking.booking_reference,
                        'guest_name': booking.guest_full_name,
                        'guest_email': booking.guest_email,
                        'villa': booking.villa.villa_type.name,
                    },
                }
            }
        }

        response = self._request('POST', '/links', payload)
        link_data = response['data']
        attributes = link_data['attributes']

        return {
            'link_id': link_data['id'],
            'checkout_url': attributes['checkout_url'],
            'status': attributes['status'],
            'reference_number': attributes.get('reference_number', ''),
        }

    def retrieve_payment_link(self, link_id):
        """Retrieve payment link status from PayMongo"""
        response = self._request('GET', f'/links/{link_id}')
        return response['data']['attributes']

    def verify_webhook(self, payload, signature_header):
        """
        Verify PayMongo webhook signature.
        PayMongo signs webhook with HMAC-SHA256.
        """
        if not self.webhook_secret:
            logger.warning('PayMongo webhook secret not configured')
            return False

        expected_sig = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_sig, signature_header)

    def process_webhook_event(self, event_type, event_data):
        """
        Process incoming PayMongo webhook events.
        Returns (booking_reference, new_status) or raises PaymentError.
        """
        from .models import Payment, Booking

        attributes = event_data.get('attributes', {})
        metadata = attributes.get('data', {}).get('attributes', {}).get('metadata', {})
        booking_reference = metadata.get('booking_reference')

        if not booking_reference:
            # Try to get from remarks
            booking_reference = attributes.get('data', {}).get('attributes', {}).get('remarks', '')

        if not booking_reference:
            raise PaymentError('Cannot determine booking reference from webhook')

        try:
            payment = Payment.objects.select_related('booking').get(
                booking__booking_reference=booking_reference
            )
        except Payment.DoesNotExist:
            raise PaymentError(f'No payment found for booking {booking_reference}')

        if event_type == 'payment.paid':
            payment.status = 'paid'
            payment.paid_at = timezone.now()
            payment.amount_paid = Decimal(str(attributes.get('data', {}).get('attributes', {}).get('amount', 0))) / 100
            payment.booking.status = 'confirmed'
            payment.booking.save()
            payment.save()
            return payment.booking, 'paid'

        elif event_type == 'payment.failed':
            payment.status = 'failed'
            payment.save()
            return payment.booking, 'failed'

        return payment.booking, 'unknown'


# ══════════════════════════════════════════════════════════
#  PAYMENT GATEWAY FACTORY
# ══════════════════════════════════════════════════════════

class PaymentError(Exception):
    pass


def get_payment_service(provider='paymongo'):
    """Factory function — returns PayMongo service"""
    return PayMongoService()


def initiate_payment(booking, provider, request):
    """
    Master function: creates a Payment record and initiates
    the payment with PayMongo.

    Returns: checkout_url for PayMongo redirect
    """
    from .models import Payment

    # Create or get Payment record
    payment, _ = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            'amount': booking.total_price,
            'provider': provider,
            'status': 'pending',
        }
    )
    payment.amount = booking.total_price
    payment.provider = provider
    payment.status = 'awaiting_payment'
    payment.save()

    service = get_payment_service(provider)
    result = service.create_payment_link(booking, request)
    payment.provider_link_id = result['link_id']
    payment.checkout_url = result['checkout_url']
    payment.save()
    
    return {'redirect_url': result['checkout_url'], 'type': 'redirect'}

