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
        'description': (
            'Step directly onto the pristine white sand from your private terrace. '
            'This intimate beachfront villa is designed for couples seeking a romantic '
            'escape with panoramic sea views from every room. Featuring a king bed, '
            'open-air bathroom, and a private daybed perched just meters from the water.'
        ),
        'short_description': 'Intimate beachfront villa with direct sand access and panoramic sea views.',
        'price_per_night': '8500.00',
        'max_guests': 2,
        'bedrooms': 1,
        'bathrooms': 1,
        'size_sqm': 65,
        'is_featured': True,
        'sort_order': 1,
        'amenities': [
            'King Bed', 'Air Conditioning', 'Private Beach Access', 'Sea View Terrace',
            'Open-Air Bathroom', 'Free WiFi', 'Daily Breakfast', 'Welcome Drinks',
            'Beach Towels', 'Kayak Access'
        ],
    },
    {
        'name': 'Lagoon Pool Suite',
        'slug': 'lagoon-pool-suite',
        'category': 'pool',
        'description': (
            'Your own private infinity pool merges seamlessly with the horizon in this '
            'stunning two-bedroom suite. Perfect for families or groups of friends, '
            'the Lagoon Pool Suite features a spacious living area, fully-stocked '
            'kitchenette, and a wraparound deck with sun loungers. The pool is heated '
            'and available 24 hours.'
        ),
        'short_description': 'Two-bedroom suite with private infinity pool and lagoon views.',
        'price_per_night': '14500.00',
        'max_guests': 4,
        'bedrooms': 2,
        'bathrooms': 2,
        'size_sqm': 110,
        'is_featured': True,
        'sort_order': 2,
        'amenities': [
            'Private Infinity Pool', 'King + Twin Beds', 'Air Conditioning',
            'Full Kitchenette', 'Sun Deck', 'Free WiFi', 'Daily Breakfast',
            'Pool Service', 'Smart TV', 'Yoga Mats', 'Snorkeling Gear'
        ],
    },
    {
        'name': 'Cliffside Grand Villa',
        'slug': 'cliffside-grand-villa',
        'category': 'cliff',
        'description': (
            'Perched dramatically above the turquoise bay, the Cliffside Grand Villa '
            'commands breathtaking 270-degree vistas of the Sulu Sea. This '
            'three-bedroom masterpiece features soaring ceilings, natural stone walls, '
            'and a cantilevered terrace that floats above the cliff edge. '
            'Private chef service available on request.'
        ),
        'short_description': '3-bedroom cliffside sanctuary with 270° ocean panoramas.',
        'price_per_night': '22000.00',
        'max_guests': 6,
        'bedrooms': 3,
        'bathrooms': 3,
        'size_sqm': 180,
        'is_featured': True,
        'sort_order': 3,
        'amenities': [
            '3 King Beds', 'Private Plunge Pool', 'Cliff-Edge Terrace',
            'Air Conditioning (all rooms)', 'Private Chef (on request)',
            'Free WiFi', 'Daily Breakfast', 'Smart Home System',
            'Private Bar', 'Telescope', 'Dedicated Butler'
        ],
    },
    {
        'name': 'Garden Bungalow',
        'slug': 'garden-bungalow',
        'category': 'garden',
        'description': (
            'Nestled within lush tropical gardens, the Garden Bungalow is a '
            'peaceful haven for solo travelers and couples who prefer tranquility '
            'over beachfront hustle. Traditional bahay kubo architecture meets '
            'modern comforts in this charming hideaway.'
        ),
        'short_description': 'Peaceful garden retreat with traditional Filipino design.',
        'price_per_night': '6800.00',
        'max_guests': 2,
        'bedrooms': 1,
        'bathrooms': 1,
        'size_sqm': 55,
        'is_featured': False,
        'sort_order': 4,
        'amenities': [
            'Queen Bed', 'Garden Terrace', 'Air Conditioning',
            'Outdoor Rain Shower', 'Free WiFi', 'Daily Breakfast',
            'Hammock', 'Garden Views'
        ],
    },
    {
        'name': 'Overwater Chalet',
        'slug': 'overwater-chalet',
        'category': 'overwater',
        'description': (
            'Experience the iconic over-water living in this extraordinary chalet '
            'built on stilts above a crystal-clear lagoon. The glass floor panel '
            'in the living room lets you watch the reef fish below. '
            'Direct ladder access into the warm shallow water from your private deck.'
        ),
        'short_description': 'Iconic overwater bungalow with glass floor and lagoon access.',
        'price_per_night': '18000.00',
        'max_guests': 2,
        'bedrooms': 1,
        'bathrooms': 1,
        'size_sqm': 72,
        'is_featured': False,
        'sort_order': 5,
        'amenities': [
            'King Bed', 'Glass Floor Panel', 'Direct Lagoon Access',
            'Overwater Deck', 'Air Conditioning', 'Free WiFi',
            'Daily Breakfast', 'Snorkeling Gear', 'Underwater Lighting',
            'Fish Feeding Station'
        ],
    },
    {
        'name': 'Sunset Paradise Villa',
        'slug': 'sunset-paradise-villa',
        'category': 'beachfront',
        'description': (
            'Perfectly oriented to capture Palawan\'s legendary sunsets, this '
            'west-facing beachfront villa is a photographer\'s and romantic\'s dream. '
            'The expansive deck with built-in fire pit is the perfect place to end '
            'each golden evening. Includes private outdoor shower and jacuzzi.'
        ),
        'short_description': 'West-facing beachfront villa with fire pit, jacuzzi, and sunsets.',
        'price_per_night': '11000.00',
        'max_guests': 4,
        'bedrooms': 2,
        'bathrooms': 2,
        'size_sqm': 90,
        'is_featured': False,
        'sort_order': 6,
        'amenities': [
            'King + Queen Beds', 'Private Jacuzzi', 'Beach Fire Pit',
            'Outdoor Shower', 'Air Conditioning', 'Free WiFi',
            'Daily Breakfast', 'Sunset Cocktail Hour', 'Beach Loungers'
        ],
    },
]

TESTIMONIALS = [
    {
        'guest_name': 'Sarah & James M.',
        'guest_country': 'Australia',
        'rating': 5,
        'text': (
            'Absolutely breathtaking. We stayed in the Ocean Breeze Villa for our '
            'honeymoon and it exceeded every expectation. Waking up to the sound of '
            'waves with the sea practically at our feet... we never wanted to leave.'
        ),
        'is_featured': True,
    },
    {
        'guest_name': 'Thomas K.',
        'guest_country': 'Germany',
        'rating': 5,
        'text': (
            'The Cliffside Grand Villa was a revelation — spectacular architecture, '
            'attentive staff, and views that made every morning feel like a painting. '
            'The private chef service was exceptional. Will return without question.'
        ),
        'is_featured': True,
    },
    {
        'guest_name': 'The Wong Family',
        'guest_country': 'Singapore',
        'rating': 5,
        'text': (
            'Perfect family holiday. The Lagoon Pool Suite had everything we needed. '
            'Kids loved the snorkeling gear and kayaks. Staff were incredibly helpful '
            'with every request. The breakfast spread each morning was outstanding.'
        ),
        'is_featured': True,
    },
    {
        'guest_name': 'Elena V.',
        'guest_country': 'France',
        'rating': 5,
        'text': (
            'The Overwater Chalet was magical — I spent an hour just watching '
            'fish through the glass floor! Ryan\'s manages to feel both luxurious '
            'and genuinely connected to nature. A rare combination done perfectly.'
        ),
        'is_featured': True,
    },
]


class Command(BaseCommand):
    help = 'Seed database with demo resort data'

    def handle(self, *args, **options):
        self.stdout.write('🌊 Seeding Ryan\'s Beach Resort data...')

        # Create villa types and units
        for data in VILLAS:
            amenities = data.pop('amenities')
            vt, created = VillaType.objects.get_or_create(
                slug=data['slug'],
                defaults={**data, 'amenities': amenities}
            )
            if created:
                self.stdout.write(f'  ✅ Created villa type: {vt.name}')
                # Create 3 units per villa type
                for i in range(1, 4):
                    Villa.objects.create(
                        villa_type=vt,
                        unit_number=f'{100 + i}',
                        floor=1 if i < 3 else 2,
                    )
            else:
                self.stdout.write(f'  → Exists: {vt.name}')

        # Create testimonials
        for t_data in TESTIMONIALS:
            _, created = Testimonial.objects.get_or_create(
                guest_name=t_data['guest_name'],
                defaults=t_data
            )
            if created:
                self.stdout.write(f'  ⭐ Created testimonial: {t_data["guest_name"]}')

        self.stdout.write(self.style.SUCCESS('\n✨ Seeding complete!'))
        self.stdout.write('Run: python manage.py createsuperuser to set up admin access.')
