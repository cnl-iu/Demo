from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resort', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(choices=[('paymongo', 'PayMongo'), ('stripe', 'Stripe'), ('manual', 'Manual / Bank Transfer')], default='paymongo', max_length=20)),
                ('method', models.CharField(blank=True, choices=[('gcash', 'GCash'), ('maya', 'Maya'), ('card', 'Credit / Debit Card'), ('bank_transfer', 'Bank Transfer'), ('grab_pay', 'GrabPay')], max_length=30)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('awaiting_payment', 'Awaiting Payment'), ('paid', 'Paid'), ('failed', 'Failed'), ('refunded', 'Refunded'), ('partially_refunded', 'Partially Refunded')], default='pending', max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('currency', models.CharField(default='PHP', max_length=5)),
                ('provider_payment_id', models.CharField(blank=True, max_length=200)),
                ('provider_link_id', models.CharField(blank=True, max_length=200)),
                ('provider_intent_id', models.CharField(blank=True, max_length=200)),
                ('checkout_url', models.URLField(blank=True)),
                ('webhook_data', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='resort.booking')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'ordering': ['-created_at'],
            },
        ),
    ]
