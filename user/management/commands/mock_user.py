from django.core.management.base import BaseCommand
from user.models import User
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Mock user'
    RANGE = 50

    def create_bulk_users(self):
        bulk = []
        for i in range(1, self.RANGE):
            me = {
                "username": f"test_user_{i}",
                "password": make_password(f"test_user_{i}")
            }
            bulk.append(User(**me))
        return User.objects.bulk_create(bulk)

    def handle(self, *args, **options):
        self.create_bulk_users()
        self.stdout.write(self.style.SUCCESS(f"Created: {self.RANGE} Users"))
