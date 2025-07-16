import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create default superuser if it doesn't exist"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = os.environ.get("DJANGO_ADMIN_EMAIL")
        username = os.environ.get("DJANGO_ADMIN_USERNAME", "admin")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not all([email, password]):
            self.stdout.write(self.style.ERROR("Missing admin credentials in environment variables."))
            return

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, username=username, password=password)
            self.stdout.write(self.style.SUCCESS("Superuser created"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))
