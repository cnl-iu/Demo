"""
Email notification service for Demo Beach Resort.

Handles:
- Guest booking confirmation
- Admin new booking alert
- Admin status change notification to guest
- Contact form auto-reply
- Admin contact message alert
- Booking cancellation notice
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_booking_confirmation_to_guest(booking):
    """
    Send confirmation email to the guest after booking is created.
    Triggered: immediately after Booking.save() in booking_step2 view.
    """
    subject = f"Booking Confirmed — {booking.booking_reference} | Demo Beach Resort"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body {{ font-family: 'Georgia', serif; background: #f5efe6; margin: 0; padding: 0; }}
        .wrapper {{ max-width: 600px; margin: 40px auto; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #0e4c5a, #1a7a8a); padding: 40px 40px 30px; text-align: center; }}
        .header h1 {{ color: #fff; font-size: 28px; margin: 0 0 6px; font-weight: 400; }}
        .header p {{ color: rgba(255,255,255,0.75); font-size: 14px; margin: 0; letter-spacing: 2px; text-transform: uppercase; }}
        .body {{ padding: 40px; }}
        .greeting {{ font-size: 18px; color: #1a1a1a; margin-bottom: 16px; }}
        .ref-box {{ background: #f5efe6; border: 2px dashed #e8ddd0; border-radius: 10px; text-align: center; padding: 24px; margin: 24px 0; }}
        .ref-label {{ font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: #6b8189; display: block; margin-bottom: 6px; }}
        .ref-number {{ font-size: 28px; font-weight: 700; color: #0e4c5a; font-family: monospace; letter-spacing: 3px; }}
        .details-grid {{ display: grid; margin: 28px 0; border: 1px solid #e8ddd0; border-radius: 10px; overflow: hidden; }}
        .detail-row {{ display: flex; border-bottom: 1px solid #e8ddd0; }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{ background: #f5efe6; padding: 14px 18px; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #6b8189; width: 40%; font-weight: 600; }}
        .detail-value {{ padding: 14px 18px; font-size: 14px; color: #1a1a1a; width: 60%; }}
        .total-row .detail-label {{ background: #0e4c5a; color: #4db8c8; }}
        .total-row .detail-value {{ background: #0e4c5a; color: #fff; font-size: 18px; font-weight: 700; font-family: Georgia, serif; }}
        .next-steps {{ background: #f5efe6; border-radius: 10px; padding: 24px; margin: 28px 0; }}
        .next-steps h3 {{ font-size: 14px; letter-spacing: 1px; text-transform: uppercase; color: #6b8189; margin: 0 0 16px; }}
        .step {{ display: flex; align-items: flex-start; gap: 14px; margin-bottom: 14px; }}
        .step-num {{ background: #0e4c5a; color: #fff; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; line-height: 26px; text-align: center; }}
        .step-text strong {{ display: block; font-size: 14px; color: #1a1a1a; margin-bottom: 2px; }}
        .step-text span {{ font-size: 13px; color: #6b8189; }}
        .special-req {{ background: #fffbeb; border-left: 3px solid #c9a84c; padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 20px 0; font-size: 14px; color: #4a5568; }}
        .footer {{ background: #0a1a22; padding: 28px 40px; text-align: center; }}
        .footer p {{ color: rgba(255,255,255,0.5); font-size: 12px; margin: 4px 0; }}
        .footer a {{ color: #4db8c8; text-decoration: none; }}
        .divider {{ border: none; border-top: 1px solid #e8ddd0; margin: 24px 0; }}
      </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="header">
          <h1>Demo Beach Resort</h1>
          <p>Booking Confirmation</p>
        </div>

        <div class="body">
          <p class="greeting">Dear {booking.guest_first_name},</p>
          <p style="color:#4a5568;font-size:15px;line-height:1.7;">
            Your reservation has been received and is currently <strong>pending confirmation</strong>.
            Our team will confirm your booking within 2 hours and send a follow-up email.
            We're looking forward to welcoming you to paradise!
          </p>

          <div class="ref-box">
            <span class="ref-label">Your Booking Reference</span>
            <div class="ref-number">{booking.booking_reference}</div>
            <p style="font-size:12px;color:#6b8189;margin:8px 0 0;">Keep this for check-in and any changes</p>
          </div>

          <div class="details-grid">
            <div class="detail-row">
              <div class="detail-label">Villa</div>
              <div class="detail-value">{booking.villa.villa_type.name}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Unit</div>
              <div class="detail-value">Unit {booking.villa.unit_number}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Check-In</div>
              <div class="detail-value">{booking.check_in.strftime('%A, %d %B %Y')} <span style="color:#6b8189;font-size:12px;">from 2:00 PM</span></div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Check-Out</div>
              <div class="detail-value">{booking.check_out.strftime('%A, %d %B %Y')} <span style="color:#6b8189;font-size:12px;">before 12:00 PM</span></div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Duration</div>
              <div class="detail-value">{booking.nights} Night{'s' if booking.nights > 1 else ''}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Guests</div>
              <div class="detail-value">{booking.adults} Adult{'s' if booking.adults > 1 else ''}{',' + str(booking.children) + ' Child' + ('ren' if booking.children > 1 else '') if booking.children else ''}</div>
            </div>
            <div class="detail-row total-row">
              <div class="detail-label">Total</div>
              <div class="detail-value">₱{booking.total_price:,.0f} <span style="font-size:12px;opacity:0.7;">incl. taxes & breakfast</span></div>
            </div>
          </div>

          {'<div class="special-req"><strong style="display:block;margin-bottom:4px;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#c9a84c;">Special Request Noted</strong>' + booking.special_requests + '</div>' if booking.special_requests else ''}

          <div class="next-steps">
            <h3>What Happens Next</h3>
            <div class="step">
              <div class="step-num">1</div>
              <div class="step-text">
                <strong>Booking Confirmation</strong>
                <span>Our team will confirm your reservation within 2 hours via email.</span>
              </div>
            </div>
            <div class="step">
              <div class="step-num">2</div>
              <div class="step-text">
                <strong>Pre-Arrival Contact</strong>
                <span>We'll reach out 48 hours before arrival to arrange transfers and confirm preferences.</span>
              </div>
            </div>
            <div class="step">
              <div class="step-num">3</div>
              <div class="step-text">
                <strong>Check-In</strong>
                <span>Arrive at resort reception. Your villa will be ready from 2:00 PM.</span>
              </div>
            </div>
          </div>

          <hr class="divider">
          <p style="font-size:13px;color:#6b8189;text-align:center;">
            Questions? Reply to this email or call us at
            <a href="tel:+639123456789" style="color:#0e4c5a;">+63 912 345 6789</a>
          </p>
        </div>

        <div class="footer">
          <p>Demo Beach Resort · Barangay Paradise Cove, El Nido, Palawan 5313</p>
          <p><a href="mailto:hello@beachresort.com">hello@beachresort.com</a> · <a href="tel:+639123456789">+63 912 345 6789</a></p>
          <p style="margin-top:12px;font-size:11px;">© 2025 Demo Beach Resort. All rights reserved.</p>
        </div>
      </div>
    </body>
    </html>
    """

    plain_body = f"""
Demo Beach Resort — Booking Confirmation

Dear {booking.guest_first_name},

Your booking reference is: {booking.booking_reference}

RESERVATION DETAILS
-------------------
Villa:      {booking.villa.villa_type.name} (Unit {booking.villa.unit_number})
Check-In:   {booking.check_in.strftime('%A, %d %B %Y')} from 2:00 PM
Check-Out:  {booking.check_out.strftime('%A, %d %B %Y')} before 12:00 PM
Duration:   {booking.nights} night(s)
Guests:     {booking.adults} adult(s){f', {booking.children} child(ren)' if booking.children else ''}
Total:      PHP {booking.total_price:,.0f} (taxes & breakfast included)

{'Special Request: ' + booking.special_requests if booking.special_requests else ''}

WHAT HAPPENS NEXT
-----------------
1. Our team will confirm your booking within 2 hours.
2. We'll contact you 48 hours before arrival.
3. Check in at reception from 2:00 PM.

Questions? Contact us:
Email: hello@beachresort.com
Phone: +63 912 345 6789

Demo Beach Resort · El Nido, Palawan, Philippines
    """

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.guest_email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)
        logger.info(f"Booking confirmation sent to {booking.guest_email} — {booking.booking_reference}")
        return True
    except Exception as e:
        logger.error(f"Failed to send booking confirmation to {booking.guest_email}: {e}")
        return False


def send_new_booking_alert_to_admin(booking):
    """
    Send alert email to resort admin when a new booking comes in.
    Triggered: immediately after Booking.save() in booking_step2 view.
    """
    subject = f"🏖 NEW BOOKING — {booking.booking_reference} | {booking.villa.villa_type.name}"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body {{ font-family: Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 20px; }}
        .wrapper {{ max-width: 600px; margin: 0 auto; background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }}
        .alert-bar {{ background: #e07050; padding: 16px 32px; color: #fff; font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }}
        .header {{ background: #0e4c5a; padding: 24px 32px; }}
        .header h2 {{ color: #fff; margin: 0; font-size: 20px; }}
        .header span {{ color: #4db8c8; font-size: 13px; }}
        .body {{ padding: 32px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
        td {{ padding: 12px 14px; border-bottom: 1px solid #e8ddd0; font-size: 14px; }}
        td:first-child {{ color: #6b8189; font-weight: 600; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; width: 35%; background: #f5efe6; }}
        .price {{ font-size: 20px; color: #0e4c5a; font-weight: 700; }}
        .btn {{ display: inline-block; background: #0e4c5a; color: #fff; padding: 12px 28px; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: 600; margin-top: 20px; }}
        .footer {{ background: #f5efe6; padding: 16px 32px; font-size: 12px; color: #6b8189; text-align: center; }}
      </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="alert-bar">⚡ New Booking Received</div>
        <div class="header">
          <h2>Booking #{booking.booking_reference}</h2>
          <span>Received: {booking.created_at.strftime('%d %B %Y at %I:%M %p')}</span>
        </div>
        <div class="body">
          <table>
            <tr><td>Guest</td><td><strong>{booking.guest_full_name}</strong></td></tr>
            <tr><td>Email</td><td><a href="mailto:{booking.guest_email}">{booking.guest_email}</a></td></tr>
            <tr><td>Phone</td><td><a href="tel:{booking.guest_phone}">{booking.guest_phone}</a></td></tr>
            <tr><td>Country</td><td>{booking.guest_country or '—'}</td></tr>
            <tr><td>Villa</td><td><strong>{booking.villa.villa_type.name}</strong> · Unit {booking.villa.unit_number}</td></tr>
            <tr><td>Check-In</td><td>{booking.check_in.strftime('%A, %d %B %Y')}</td></tr>
            <tr><td>Check-Out</td><td>{booking.check_out.strftime('%A, %d %B %Y')}</td></tr>
            <tr><td>Nights</td><td>{booking.nights}</td></tr>
            <tr><td>Guests</td><td>{booking.adults} adult(s){f', {booking.children} child(ren)' if booking.children else ''}</td></tr>
            <tr><td>Total</td><td><span class="price">₱{booking.total_price:,.0f}</span></td></tr>
            {'<tr><td>Special Req.</td><td style="color:#c9a84c;">' + booking.special_requests + '</td></tr>' if booking.special_requests else ''}
            <tr><td>Status</td><td><strong style="color:#e07050;">PENDING — Action Required</strong></td></tr>
          </table>
          <a href="http://127.0.0.1:8000/admin/resort/booking/" class="btn">View in Admin Dashboard →</a>
        </div>
        <div class="footer">Demo Beach Resort Admin Notification System</div>
      </div>
    </body>
    </html>
    """

    plain_body = f"""
NEW BOOKING ALERT — Demo Beach Resort

Booking Reference: {booking.booking_reference}
Status: PENDING — Action Required

GUEST DETAILS
Guest:    {booking.guest_full_name}
Email:    {booking.guest_email}
Phone:    {booking.guest_phone}
Country:  {booking.guest_country or 'N/A'}

RESERVATION
Villa:     {booking.villa.villa_type.name} (Unit {booking.villa.unit_number})
Check-In:  {booking.check_in.strftime('%d %B %Y')}
Check-Out: {booking.check_out.strftime('%d %B %Y')}
Nights:    {booking.nights}
Guests:    {booking.adults} adult(s)
Total:     PHP {booking.total_price:,.0f}

{'Special Request: ' + booking.special_requests if booking.special_requests else ''}

Login to Admin: http://127.0.0.1:8000/admin/resort/booking/
    """

    admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)
        logger.info(f"Admin alert sent for booking {booking.booking_reference}")
        return True
    except Exception as e:
        logger.error(f"Failed to send admin booking alert: {e}")
        return False


def send_booking_status_update_to_guest(booking):
    """
    Notify guest when admin changes booking status
    (confirmed / cancelled).
    Triggered: in admin action or status change signal.
    """
    status_config = {
        'confirmed': {
            'subject': f"✅ Booking Confirmed — {booking.booking_reference} | Demo Beach Resort",
            'color': '#27ae60',
            'emoji': '✅',
            'headline': 'Your Booking is Confirmed!',
            'message': f"""
                Great news, {booking.guest_first_name}! Your reservation has been officially confirmed.
                We can't wait to welcome you to Demo Beach Resort.
                Please save your booking reference for check-in.
            """,
        },
        'cancelled': {
            'subject': f"Booking Cancelled — {booking.booking_reference} | Demo Beach Resort",
            'color': '#c0392b',
            'emoji': '❌',
            'headline': 'Your Booking Has Been Cancelled',
            'message': f"""
                Dear {booking.guest_first_name}, your reservation ({booking.booking_reference})
                has been cancelled. If you believe this is an error or would like to rebook,
                please contact us at hello@beachresort.com or call +63 912 345 6789.
            """,
        },
    }

    cfg = status_config.get(booking.status)
    if not cfg:
        return False

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8">
    <style>
      body {{ font-family: Georgia, serif; background: #f5efe6; margin: 0; padding: 20px; }}
      .wrapper {{ max-width: 600px; margin: 0 auto; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
      .header {{ background: {cfg['color']}; padding: 36px; text-align: center; color: #fff; }}
      .header .emoji {{ font-size: 48px; display: block; margin-bottom: 12px; }}
      .header h2 {{ margin: 0; font-size: 24px; font-weight: 400; }}
      .body {{ padding: 36px; }}
      .ref-box {{ background: #f5efe6; border-radius: 10px; text-align: center; padding: 20px; margin: 20px 0; }}
      .ref-num {{ font-family: monospace; font-size: 24px; color: #0e4c5a; font-weight: 700; letter-spacing: 3px; }}
      table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
      td {{ padding: 12px 14px; border-bottom: 1px solid #e8ddd0; font-size: 14px; }}
      td:first-child {{ color: #6b8189; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; width: 35%; background: #f5efe6; }}
      .footer {{ background: #0a1a22; padding: 24px; text-align: center; color: rgba(255,255,255,0.5); font-size: 12px; }}
      .footer a {{ color: #4db8c8; text-decoration: none; }}
    </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="header">
          <span class="emoji">{cfg['emoji']}</span>
          <h2>{cfg['headline']}</h2>
        </div>
        <div class="body">
          <p style="font-size:15px;color:#4a5568;line-height:1.7;">{cfg['message']}</p>
          <div class="ref-box">
            <div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#6b8189;margin-bottom:6px;">Booking Reference</div>
            <div class="ref-num">{booking.booking_reference}</div>
          </div>
          <table>
            <tr><td>Villa</td><td>{booking.villa.villa_type.name}</td></tr>
            <tr><td>Check-In</td><td>{booking.check_in.strftime('%A, %d %B %Y')}</td></tr>
            <tr><td>Check-Out</td><td>{booking.check_out.strftime('%A, %d %B %Y')}</td></tr>
            <tr><td>Nights</td><td>{booking.nights}</td></tr>
            <tr><td>Total</td><td>₱{booking.total_price:,.0f}</td></tr>
          </table>
          <p style="font-size:13px;color:#6b8189;text-align:center;">
            Need help? <a href="mailto:hello@beachresort.com" style="color:#0e4c5a;">hello@beachresort.com</a>
            · <a href="tel:+639123456789" style="color:#0e4c5a;">+63 912 345 6789</a>
          </p>
        </div>
        <div class="footer">
          <p>Demo Beach Resort · El Nido, Palawan, Philippines</p>
          <p><a href="mailto:hello@beachresort.com">hello@beachresort.com</a></p>
        </div>
      </div>
    </body>
    </html>
    """

    plain_body = f"""
Demo Beach Resort — {cfg['headline']}

{cfg['message']}

Booking Reference: {booking.booking_reference}
Villa: {booking.villa.villa_type.name}
Check-In: {booking.check_in.strftime('%d %B %Y')}
Check-Out: {booking.check_out.strftime('%d %B %Y')}

Contact us: hello@beachresort.com | +63 912 345 6789
    """

    try:
        email = EmailMultiAlternatives(
            subject=cfg['subject'],
            body=plain_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.guest_email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)
        logger.info(f"Status update ({booking.status}) sent to {booking.guest_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send status update email: {e}")
        return False


def send_contact_autoreply_to_guest(contact_message):
    """
    Send auto-reply to guest who submitted the contact form.
    Triggered: in contact view after ContactMessage.save().
    """
    subject = f"We received your message — Demo Beach Resort"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8">
    <style>
      body {{ font-family: Georgia, serif; background: #f5efe6; margin: 0; padding: 20px; }}
      .wrapper {{ max-width: 600px; margin: 0 auto; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
      .header {{ background: linear-gradient(135deg, #0e4c5a, #1a7a8a); padding: 36px; text-align: center; }}
      .header h2 {{ color: #fff; margin: 0; font-size: 22px; font-weight: 400; }}
      .header p {{ color: rgba(255,255,255,0.7); font-size: 13px; margin: 6px 0 0; letter-spacing: 2px; text-transform: uppercase; }}
      .body {{ padding: 36px; }}
      .msg-box {{ background: #f5efe6; border-left: 3px solid #4db8c8; padding: 16px 20px; border-radius: 0 8px 8px 0; margin: 20px 0; font-size: 14px; color: #4a5568; font-style: italic; line-height: 1.7; }}
      .contact-grid {{ display: flex; gap: 16px; margin: 24px 0; }}
      .contact-item {{ flex: 1; text-align: center; background: #f5efe6; border-radius: 8px; padding: 16px; }}
      .contact-item .icon {{ font-size: 24px; }}
      .contact-item strong {{ display: block; font-size: 13px; color: #1a1a1a; margin: 6px 0 2px; }}
      .contact-item span {{ font-size: 12px; color: #6b8189; }}
      .footer {{ background: #0a1a22; padding: 24px; text-align: center; color: rgba(255,255,255,0.5); font-size: 12px; }}
      .footer a {{ color: #4db8c8; }}
    </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="header">
          <h2>Demo Beach Resort</h2>
          <p>Message Received</p>
        </div>
        <div class="body">
          <p style="font-size:16px;color:#1a1a1a;">Dear {contact_message.name},</p>
          <p style="color:#4a5568;font-size:15px;line-height:1.7;">
            Thank you for reaching out! We've received your message and our team
            will get back to you within <strong>2 hours</strong> during business hours
            (8AM–10PM Philippine Time).
          </p>

          <p style="font-size:13px;color:#6b8189;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">
            Your message:
          </p>
          <div class="msg-box">
            <strong style="color:#0e4c5a;font-style:normal;display:block;margin-bottom:6px;">{contact_message.subject}</strong>
            {contact_message.message}
          </div>

          <p style="color:#4a5568;font-size:14px;">Need immediate assistance? Reach us directly:</p>
          <div class="contact-grid">
            <div class="contact-item">
              <div class="icon">📞</div>
              <strong>+63 912 345 6789</strong>
              <span>Available 24/7</span>
            </div>
            <div class="contact-item">
              <div class="icon">✉️</div>
              <strong>hello@beachresort.com</strong>
              <span>Reply to this email</span>
            </div>
            <div class="contact-item">
              <div class="icon">🕐</div>
              <strong>8AM – 10PM PHT</strong>
              <span>Office hours</span>
            </div>
          </div>
        </div>
        <div class="footer">
          <p>Demo Beach Resort · El Nido, Palawan, Philippines 5313</p>
          <p><a href="mailto:hello@beachresort.com">hello@beachresort.com</a></p>
        </div>
      </div>
    </body>
    </html>
    """

    plain_body = f"""
Demo Beach Resort — Message Received

Dear {contact_message.name},

Thank you for reaching out! We'll respond within 2 hours.

Your message:
Subject: {contact_message.subject}
{contact_message.message}

Contact us directly:
Phone: +63 912 345 6789 (24/7)
Email: hello@beachresort.com

Demo Beach Resort · El Nido, Palawan, Philippines
    """

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[contact_message.email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)
        logger.info(f"Contact auto-reply sent to {contact_message.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send contact auto-reply: {e}")
        return False


def send_contact_alert_to_admin(contact_message):
    """
    Notify admin of new contact form submission.
    Triggered: in contact view after ContactMessage.save().
    """
    subject = f"💬 New Contact Message — {contact_message.subject}"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8">
    <style>
      body {{ font-family: Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 20px; }}
      .wrapper {{ max-width: 560px; margin: 0 auto; background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }}
      .header {{ background: #1a6b7a; padding: 20px 28px; color: #fff; font-size: 14px; }}
      .body {{ padding: 28px; }}
      table {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}
      td {{ padding: 10px 14px; border-bottom: 1px solid #e8ddd0; font-size: 14px; }}
      td:first-child {{ color: #6b8189; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; width: 30%; background: #f5efe6; }}
      .msg {{ background: #f5efe6; padding: 16px; border-radius: 8px; font-size: 14px; line-height: 1.7; color: #4a5568; margin: 16px 0; }}
      .btn {{ display: inline-block; background: #0e4c5a; color: #fff; padding: 10px 24px; border-radius: 6px; text-decoration: none; font-size: 14px; }}
      .footer {{ background: #f5efe6; padding: 14px 28px; font-size: 12px; color: #6b8189; }}
    </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="header">💬 New Contact Message Received</div>
        <div class="body">
          <table>
            <tr><td>Name</td><td><strong>{contact_message.name}</strong></td></tr>
            <tr><td>Email</td><td><a href="mailto:{contact_message.email}">{contact_message.email}</a></td></tr>
            {'<tr><td>Phone</td><td>' + contact_message.phone + '</td></tr>' if contact_message.phone else ''}
            <tr><td>Subject</td><td><strong>{contact_message.subject}</strong></td></tr>
            <tr><td>Received</td><td>{contact_message.created_at.strftime('%d %B %Y at %I:%M %p')}</td></tr>
          </table>
          <div class="msg">{contact_message.message}</div>
          <a href="http://127.0.0.1:8000/admin/resort/contactmessage/" class="btn">View in Admin →</a>
        </div>
        <div class="footer">Demo Beach Resort Admin Notification</div>
      </div>
    </body>
    </html>
    """

    plain_body = f"""
New Contact Message — Demo Beach Resort

From:     {contact_message.name}
Email:    {contact_message.email}
Phone:    {contact_message.phone or 'N/A'}
Subject:  {contact_message.subject}

Message:
{contact_message.message}

Admin: http://127.0.0.1:8000/admin/resort/contactmessage/
    """

    admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)
        logger.info(f"Contact admin alert sent for {contact_message.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send contact admin alert: {e}")
        return False
