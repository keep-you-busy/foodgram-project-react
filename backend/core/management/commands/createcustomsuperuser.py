import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from users.models import User

load_dotenv()


class Command(BaseCommand):
    help = 'Creates basic a superuser if not exists'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                email=os.getenv('SUPERUSER_EMAIL', 'admin@admin.com'),
                username=os.getenv('SUPERUSER_USERNAME', 'admin'),
                first_name=os.getenv('SUPERUSER_FIRST_NAME', 'admin'),
                last_name=os.getenv('SUPERUSER_LAST_NAME', 'admin'),
                password=os.getenv('SUPERUSER_PASSWORD', 'admin')
            )
            self.stdout.write(
                self.style.SUCCESS(
                    'Superuser created successfully'
                    )
            )
        else:
            self.stdout.write(
                self.style.NOTICE(
                    'Superuser already exists'
                    )
            )
