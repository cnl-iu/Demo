# 🌊 Demo Beach Resort — Full-Stack Django Web Application

Web application for a luxury beachfront resort in Palawan, Philippines.

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
Demo_resort/
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

## 💳 Payment Integration (PayMongo)

### Supported Payment Methods
- **GCash** — instant e-wallet payment
- **Maya** (formerly PayMaya) — e-wallet payment
- **GrabPay** — e-wallet payment
- **Credit/Debit Cards** — Visa, Mastercard, JCB


---

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

**Components:**
- Responsive navigation with mobile menu
- Hero search bar with date pickers
- Villa cards with hover effects
- Multi-step booking progress indicator
- Interactive calendar availability
- Payment method selection cards
- Receipt-style confirmation pages

---

## 🧪 Testing

### Test Booking Flow (Without Payment)

1. Visit homepage → Search for dates
2. Select a villa → Continue
3. Fill guest details → Confirm
4. View payment page


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
- Email: admin@Demobeachresort.com
- Phone: +63 912 345 6789

---

## 📄 License

Proprietary — Demo Beach Resort © 2025
