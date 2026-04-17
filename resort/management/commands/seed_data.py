"""
Management command to populate the database with demo resort data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from resort.models import VillaType, Villa, Testimonial


VILLAS = [
    {
        'name': 'Ocean Breeze Villa',
        'slug': 'ocean-breeze-villa',
        'category': 'beachfront',
        'description': 'Step directly onto the pristine white sand from your private terrace. This intimate beachfront villa is designed for couples seeking a romantic escape with panoramic sea views from every room.',
        'short_description': 'Intimate beachfront villa with direct sand access and panoramic sea views.',
        'price_per_night': '8500.00',
        'max_guests': 2,
        'bedrooms': 1,
        'bathrooms': 1,
        'size_sqm': 65,
        'is_featured': True,
        'sort_order': 1,
        'amenities': ['King Bed', 'Air Conditioning', 'Private Beach Access', 'Sea View Terrace', 'Free WiFi', 'Daily Breakfast'],
    },
    {
        'name': 'Lagoon Pool Suite',
        'slug': 'lagoon-pool-suite',
        'category': 'pool',
        'description': 'Your own private infinity pool merges seamlessly with the horizon. Perfect for families, the Lagoon Pool Suite features a spacious living area and wraparound deck.',
        'short_description': 'Two-bedroom suite with private infinity pool and lagoon views.',
        'price_per_night': '14500.00',
        'max_guests': 4,
        'bedrooms': 2,
        'bathrooms': 2,
        'size_sqm': 110,
        'is_featured': True,
        'sort_order': 2,
        'amenities': ['Private Infinity Pool', 'King + Twin Beds', 'Air Conditioning', 'Full Kitchenette', 'Free WiFi', 'Daily Breakfast'],
    },
    {
        'name': 'Cliffside Grand Villa',
        'slug': 'cliffside-grand-villa',
        'category': 'cliff',
        'description': 'Perched dramatically above the turquoise bay, the Cliffside Grand Villa commands breathtaking 270-degree vistas of the Sulu Sea.',
        'short_description': '3-bedroom cliffside sanctuary with 270 degree ocean panoramas.',
        'price_per_night': '22000.00',
        'max_guests': 6,
        'bedrooms': 3,
        'bathrooms': 3,
        'size_sqm': 180,
        'is_featured': True,
        'sort_order': 3,
        'amenities': ['3 King Beds', 'Private Plunge Pool', 'Cliff-Edge Terrace', 'Air Conditioning', 'Free WiFi', 'Dedicated Butler'],
    },
    {
        'name': 'Garden Bungalow',
        'slug': 'garden-bungalow',
        'category': 'garden',
        'description': 'Nestled within lush tropical gardens, the Garden Bungalow is a peaceful haven. Traditional bahay kubo architecture meets modern comforts.',
        'short_description': 'Peaceful garden retreat with traditional Filipino design.',
        'price_per_night': '6800.00',
        'max_guests': 2,
        'bedrooms': 1,
        'bathrooms': 1,
        'size_sqm': 55,
        'is_featured': False,
        'sort_order': 4,
        'amenities': ['Queen Bed', 'Garden Terrace', 'Air Conditioning', 'Outdoor Rain Shower', 'Free WiFi', 'Daily Breakfast'],
    },
]

TESTIMONIALS = [
    {'guest_name': 'Sarah & James M.', 'guest_country': 'Australia', 'rating': 5, 'text': 'Absolutely breathtaking. We stayed in the Ocean Breeze Villa for our honeymoon and it exceeded every expectation.', 'is_featured': True},
    {'guest_name': 'Thomas K.', 'guest_country': 'Germany', 'rating': 5, 'text': 'The Cliffside Grand Villa was a revelation. Spectacular architecture, attentive staff, and views that made every morning feel like a painting.', 'is_featured': True},
    {'guest_name': 'The Wong Family', 'guest_country': 'Singapore', 'rating': 5, 'text': 'Perfect family holiday. The Lagoon Pool Suite had everything we needed. Kids loved the snorkeling gear and kayaks.', 'is_featured': True},
    {'guest_name': 'Elena V.', 'guest_country': 'France', 'rating': 5, 'text': "Ryan's manages to feel both luxurious and genuinely connected to nature. A rare combination done perfectly.", 'is_featured': True},
]


class Command(BaseCommand):
    help = 'Seed database with demo resort data'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Ryan's Beach Resort data...")
        for data in VILLAS:
            amenities = data.pop('amenities')
            vt, created = VillaType.objects.get_or_create(slug=data['slug'], defaults={**data, 'amenities': amenities})
            if created:
                self.stdout.write(f'  Created: {vt.name}')
                for i in range(1, 4):
                    Villa.objects.create(villa_type=vt, unit_number=f'{100 + i}', floor=1)
        for t_data in TESTIMONIALS:
            _, created = Testimonial.objects.get_or_create(guest_name=t_data['guest_name'], defaults=t_data)
            if created:
                self.stdout.write(f'  Testimonial: {t_data["guest_name"]}')
        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
