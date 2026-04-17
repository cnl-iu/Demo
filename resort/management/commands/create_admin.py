from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        email = "supportbizsync@gmail.com"
        username = "admin"
        password = "admin"

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                username=username,
                password=password
            )
            self.stdout.write("✅ Superuser created")
        else:
            self.stdout.write("⚠️ Superuser already exists")