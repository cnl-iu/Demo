from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resort', '0002_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='provider',
            field=models.CharField(
                choices=[
                    ('paymongo', 'PayMongo'),
                    ('manual', 'Manual / Bank Transfer')
                ],
                default='paymongo',
                max_length=20
            ),
        ),
    ]
