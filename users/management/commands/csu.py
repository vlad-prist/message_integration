from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.com',
            first_name='Admin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('admin123456')
        user.save()
