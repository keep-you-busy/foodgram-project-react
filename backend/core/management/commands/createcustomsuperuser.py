import os as operating_system

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from users.models import User

load_dotenv()


class Command(BaseCommand):
    help = 'Creates basic a superuser if not exists'
    requires_migrations_checks = True

    @staticmethod
    def create_custom_superuser(user_model):
        if not user_model.objects.filter(username='admin').exists():
            user_model.objects.create_superuser(
                email=operating_system.getenv(
                    'SUPERUSER_EMAIL', 'admin@admin.com'
                ),
                username=operating_system.getenv(
                    'SUPERUSER_USERNAME', 'admin'
                ),
                first_name=operating_system.getenv(
                    'SUPERUSER_FIRST_NAME', 'admin'
                ),
                last_name=operating_system.getenv(
                    'SUPERUSER_LAST_NAME', 'admin'
                ),
                password=operating_system.getenv(
                    'SUPERUSER_PASSWORD', 'admin'
                )
            )
            return True
        return False

    def handle(self, *args, **options):
        if self.create_custom_superuser(User):
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
