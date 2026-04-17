from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='VillaType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.CharField(choices=[('beachfront', 'Beachfront'), ('garden', 'Garden View'), ('pool', 'Pool Access'), ('cliff', 'Cliffside'), ('overwater', 'Overwater')], default='beachfront', max_length=20)),
                ('description', models.TextField()),
                ('short_description', models.CharField(max_length=255)),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_guests', models.PositiveIntegerField(default=2)),
                ('bedrooms', models.PositiveIntegerField(default=1)),
                ('bathrooms', models.PositiveIntegerField(default=1)),
                ('size_sqm', models.PositiveIntegerField(help_text='Size in square meters')),
                ('image', models.ImageField(blank=True, null=True, upload_to='villas/')),
                ('image_gallery', models.JSONField(blank=True, default=list)),
                ('amenities', models.JSONField(default=list, help_text='List of amenity strings')),
                ('is_featured', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('sort_order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['sort_order', 'name'], 'verbose_name': 'Villa Type', 'verbose_name_plural': 'Villa Types'},
        ),
        migrations.CreateModel(
            name='Villa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_number', models.CharField(max_length=20)),
                ('floor', models.PositiveIntegerField(default=1)),
                ('notes', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('villa_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='villas', to='resort.villatype')),
            ],
            options={'ordering': ['unit_number']},
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_reference', models.CharField(max_length=20, unique=True)),
                ('guest_first_name', models.CharField(max_length=100)),
                ('guest_last_name', models.CharField(max_length=100)),
                ('guest_email', models.EmailField()),
                ('guest_phone', models.CharField(max_length=20)),
                ('guest_country', models.CharField(blank=True, max_length=100)),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('adults', models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1)])),
                ('children', models.PositiveIntegerField(default=0)),
                ('special_requests', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('nights', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('villa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='resort.villa')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField()),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_name', models.CharField(max_length=100)),
                ('guest_country', models.CharField(max_length=100)),
                ('rating', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('text', models.TextField()),
                ('is_featured', models.BooleanField(default=False)),
                ('date_of_stay', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('villa_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='testimonials', to='resort.villatype')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterUniqueTogether(name='villa', unique_together={('villa_type', 'unit_number')}),
    ]
