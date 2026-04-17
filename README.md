# 🌊 Demo Beach Resort — Full-Stack Django Web Application

A production-ready Django + PostgreSQL web application for a luxury beachfront resort in Palawan, Philippines.

**Features:**
- 🏖️ Villa browsing & real-time availability search
- 📅 Multi-step booking flow with guest details
- 💳 **PayMongo payment integration** (GCash, Maya, GrabPay, Cards)
- 📧 Automated email notifications (booking confirmations, admin alerts)
- 🎨 Luxury coastal design (responsive, mobile-first)
- 🛠️ Full admin dashboard for staff

---

## 🗂 Project Structure

```
ryans_resort/
├── config/                    # Django project settings
│   ├── settings.py            # Main settings (env-driven)
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py                # WSGI entry point
├── resort/                    # Main application
│   ├── models.py              # VillaType, Villa, Booking, Payment, Contact, Testimonial
│   ├── views.py               # Main page views + API endpoints
│   ├── payment_views.py       # Payment checkout, success, webhooks
│   ├── payment_service.py     # PayMongo API integration
│   ├── emails.py              # Email notification system
│   ├── forms.py               # BookingForm, ContactForm
│   ├── urls.py                # App URL patterns
│   ├── admin.py               # Django Admin customization
│   ├── templates/resort/      # All HTML templates
│   │   ├── base.html          # Base layout (nav, footer)
│   │   ├── home.html          # Homepage with hero search
│   │   ├── accommodations.html     # Villa listings
│   │   ├── villa_detail.html       # Single villa page
│   │   ├── find_accommodation.html # Availability calendar
│   │   ├── booking_step1.html      # Booking Step 1: Select villa
│   │   ├── booking_step2.html      # Booking Step 2: Guest details
│   │   ├── payment_checkout.html   # Booking Step 3: Payment methods
│   │   ├── payment_success.html    # Booking Step 4: Confirmation
│   │   ├── payment_cancel.html     # Payment failed/cancelled
│   │   ├── contact.html            # Contact & map
│   │   ├── terms.html              # Terms & Conditions
│   │   └── booking_policy.html     # Booking Policy
│   ├── static/
│   │   ├── css/main.css       # Full stylesheet (luxury coastal aesthetic)
│   │   └── js/main.js         # Navigation, animations, booking logic
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_payment.py
│   │   └── 0003_update_payment_providers.py
│   └── management/commands/
│       └── seed_data.py       # Demo data seeder
├── requirements.txt
├── .env.example               # Environment template
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Requires:**
- Python 3.10+
- PostgreSQL 14+

---

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ryans_resort

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (Gmail example)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Ryan's Beach Resort <noreply@ryansbeachresort.com>
ADMIN_EMAIL=admin@ryansbeachresort.com

# PayMongo (Get from dashboard.paymongo.com)
PAYMONGO_PUBLIC_KEY=pk_test_xxxxxxxxxxxxx
PAYMONGO_SECRET_KEY=sk_test_xxxxxxxxxxxxx
PAYMONGO_WEBHOOK_SECRET=whsk_xxxxxxxxxxxxx
```

---

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb ryans_resort

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load demo data (optional)
python manage.py seed_data
```

---

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

Admin: `http://127.0.0.1:8000/admin/`

---

## 💳 Payment Integration (PayMongo)

### Supported Payment Methods
- **GCash** — instant e-wallet payment
- **Maya** (formerly PayMaya) — e-wallet payment
- **GrabPay** — e-wallet payment
- **Credit/Debit Cards** — Visa, Mastercard, JCB

### Setup PayMongo

1. **Create PayMongo Account:**
   - Go to https://dashboard.paymongo.com/
   - Sign up and verify your account

2. **Get API Keys:**
   - Navigate to **Developers → API Keys**
   - Copy your **Public Key** and **Secret Key**
   - For test mode, use `pk_test_xxx` and `sk_test_xxx`

3. **Configure Webhooks:**
   - Go to **Developers → Webhooks**
   - Create a new webhook endpoint:
     - **URL:** `https://yourdomain.com/webhooks/paymongo/`
     - **Events:** Select `payment.paid` and `payment.failed`
   - Copy the **Webhook Secret** (starts with `whsk_`)

4. **Add to `.env`:**
```env
PAYMONGO_PUBLIC_KEY=pk_test_your_public_key_here
PAYMONGO_SECRET_KEY=sk_test_your_secret_key_here
PAYMONGO_WEBHOOK_SECRET=whsk_your_webhook_secret_here
```

5. **Test Payment Flow:**
   - PayMongo provides test card numbers: https://developers.paymongo.com/docs/testing
   - Test GCash: Use any mobile number in test mode
   - Test card: `4343 4343 4343 4345` (Visa)

---

## 📧 Email Configuration

### Gmail Setup (Recommended for Development)

1. **Enable 2-Step Verification:**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Create App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (custom name)"
   - Copy the 16-character password

3. **Update `.env`:**
```env
EMAIL_HOST_USER=yourgmail@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
ADMIN_EMAIL=youradmin@gmail.com
```

### Email Types Sent

| Trigger | Recipient | Purpose |
|---------|-----------|---------|
| Booking created | Guest | Booking confirmation with reference number |
| Booking created | Admin | New booking alert with guest details |
| Payment successful | Guest | Payment receipt + booking confirmed |
| Status changed by admin | Guest | Status update notification |
| Contact form submitted | Guest | Auto-reply acknowledgment |
| Contact form submitted | Admin | New inquiry alert |

---

## 🎨 Design System

**Color Palette:**
- Ocean: `#0e4c5a` (Primary)
- Sand: `#f5f1e8` (Background)
- Charcoal: `#2d2d2d` (Text)
- Mist: `#6b7280` (Secondary text)

**Typography:**
- Display: Cormorant Garamond (serif)
- Body: Jost (sans-serif)

**Components:**
- Responsive navigation with mobile menu
- Hero search bar with date pickers
- Villa cards with hover effects
- Multi-step booking progress indicator
- Interactive calendar availability
- Payment method selection cards
- Receipt-style confirmation pages

---

## 📊 Database Models

### VillaType
Villa categories (Beachfront, Pool Access, Cliffside, etc.)
- Name, description, pricing
- Max guests, bedrooms, bathrooms
- Amenities (JSON array)
- Image gallery

### Villa
Individual villa units
- Foreign key to VillaType
- Unit number, floor
- Availability tracking

### Booking
Guest reservations
- Guest details (name, email, phone, country)
- Check-in/out dates, adults, children
- Status: pending, confirmed, cancelled, completed
- Special requests
- Auto-generated booking reference (RBR + 7 chars)

### Payment
Payment records linked to bookings
- Provider: PayMongo or manual
- Method: GCash, Maya, GrabPay, card, bank transfer
- Status: pending, awaiting_payment, paid, failed, refunded
- Amount, amount paid, currency
- Provider-specific IDs (link_id, payment_id)
- Webhook data storage

### ContactMessage
Contact form submissions
- Name, email, phone, subject, message
- Read/unread status

### Testimonial
Guest reviews
- Guest name, country, rating (1-5 stars)
- Review text, villa type reference
- Featured flag for homepage

---

## 🛠️ Admin Dashboard Features

Access at `/admin/`

**Villa Management:**
- Create/edit villa types
- Manage individual units
- Upload images and set amenities
- Toggle availability

**Booking Management:**
- View all bookings with filters
- Change booking status
- Send status update emails
- Search by reference, guest name, email

**Payment Tracking:**
- View all payments with status
- Filter by provider, method, date
- See PayMongo transaction IDs
- Webhook logs

**Content Management:**
- Approve/edit testimonials
- Manage contact messages
- Mark messages as read

---

## 🧪 Testing

### Test Booking Flow (Without Payment)

1. Visit homepage → Search for dates
2. Select a villa → Continue
3. Fill guest details → Confirm
4. View payment page

If PayMongo keys not configured, manual payment instructions shown.

### Test with PayMongo (Test Mode)

```env
PAYMONGO_SECRET_KEY=sk_test_xxxxx
```

Use PayMongo test credentials:
- **Test Card:** 4343 4343 4343 4345
- **Expiry:** Any future date
- **CVC:** Any 3 digits
- **Test GCash:** Any 11-digit mobile number

---

## 🚀 Production Deployment

### Environment Checklist

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=long-random-production-key

# Switch to live PayMongo keys
PAYMONGO_PUBLIC_KEY=pk_live_xxxxx
PAYMONGO_SECRET_KEY=sk_live_xxxxx
PAYMONGO_WEBHOOK_SECRET=whsk_live_xxxxx

# Production email (SendGrid, Mailgun, or SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

### Static Files

```bash
python manage.py collectstatic
```

### Security Headers

Set up:
- HTTPS/SSL certificate
- CSRF protection (enabled by default)
- Secure cookies
- HSTS headers

### Database Backups

```bash
pg_dump ryans_resort > backup_$(date +%Y%m%d).sql
```

---

## 📝 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/availability/` | GET | Check villa availability |
| `/api/booked-dates/` | GET | Get booked dates for calendar |
| `/api/price/` | GET | Calculate price for date range |

---

## 🔗 URLs Overview

**Public Pages:**
- `/` — Homepage
- `/accommodations/` — All villas
- `/accommodations/<slug>/` — Villa details
- `/find/` — Availability search
- `/contact/` — Contact form

**Booking Flow:**
- `/book/` — Step 1: Select villa & dates
- `/book/details/` — Step 2: Guest details
- `/book/payment/<ref>/` — Step 3: Payment method
- `/book/payment/<ref>/paymongo/` — Initiate PayMongo
- `/book/payment/<ref>/success/` — Payment success
- `/book/payment/<ref>/cancel/` — Payment cancelled

**Webhooks:**
- `/webhooks/paymongo/` — PayMongo payment notifications

---

## 🎯 Key Features Implemented

✅ Real-time availability checking
✅ Multi-step booking process
✅ PayMongo payment gateway (GCash, Maya, GrabPay, Cards)
✅ Automated email notifications
✅ Webhook handling for payment confirmations
✅ Responsive mobile-first design
✅ Admin dashboard with full CRUD
✅ Session-based booking cart
✅ Booking reference generation
✅ Calendar-based date selection
✅ Dynamic pricing calculation

---

## 📞 Support

For issues or questions:
- Email: admin@ryansbeachresort.com
- Phone: +63 912 345 6789

---

## 📄 License

Proprietary — Ryan's Beach Resort © 2026
