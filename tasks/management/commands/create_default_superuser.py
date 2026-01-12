import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create a default superuser from env vars if none exists"

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS("Superuser already exists. Skipping."))
            return

        username = os.environ.get("ADMIN_USERNAME")
        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not username or not email or not password:
            self.stdout.write(self.style.WARNING(
                "ENV vars ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD not set. Skipping superuser creation."
            ))
            return

        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create superuser: {e}"))
