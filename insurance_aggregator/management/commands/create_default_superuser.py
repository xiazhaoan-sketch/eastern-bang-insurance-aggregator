"""
Custom command to create a Django superuser from environment variables.

Render deploy hooks are non-interactive, so this command enables provisioning
an initial admin account automatically when `DJANGO_SUPERUSER_*` variables are
present. Running it locally is optional but convenient for automation scripts.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Create a default superuser if it does not exist using "
        "DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD, and "
        "optional DJANGO_SUPERUSER_EMAIL environment variables."
    )

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Skipping superuser creation; '
                    'DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set.',
                )
            )
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" already exists.')
            )
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(
            self.style.SUCCESS(
                f'Superuser "{username}" created successfully.'
            )
        )
