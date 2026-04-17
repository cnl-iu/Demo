from django.urls import path
from . import views
from . import payment_views

urlpatterns = [
    # Main pages
    path('', views.homepage, name='homepage'),
    path('accommodations/', views.accommodations, name='accommodations'),
    path('accommodations/<slug:slug>/', views.villa_detail, name='villa_detail'),
    path('find/', views.find_accommodation, name='find_accommodation'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms_conditions, name='terms_conditions'),
    path('booking-policy/', views.booking_policy, name='booking_policy'),

    # Booking flow
    path('book/', views.booking_step1, name='booking_step1'),
    path('book/details/', views.booking_step2, name='booking_step2'),
    path('book/confirmation/', views.booking_confirmation, name='booking_confirmation'),

    # Payment flow
    path('book/payment/<str:booking_reference>/', payment_views.payment_checkout, name='payment_checkout'),
    path('book/payment/<str:booking_reference>/paymongo/', payment_views.payment_initiate_paymongo, name='payment_initiate_paymongo'),
    path('book/payment/<str:booking_reference>/success/', payment_views.payment_success, name='payment_success'),
    path('book/payment/<str:booking_reference>/cancel/', payment_views.payment_cancel, name='payment_cancel'),

    # Webhooks
    path('webhooks/paymongo/', payment_views.webhook_paymongo, name='webhook_paymongo'),

    # API endpoints
    path('api/availability/', views.api_check_availability, name='api_check_availability'),
    path('api/booked-dates/', views.api_booked_dates, name='api_booked_dates'),
    path('api/price/', views.api_price_estimate, name='api_price_estimate'),
]
