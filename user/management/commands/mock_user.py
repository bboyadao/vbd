from django.core.management.base import BaseCommand
from user.models import User
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Mock user'
    RANGE = 50

    def add_arguments(self, parser):
        parser.add_argument('-l', '--len', type=int, help='number of user', )

    def create_bulk_users(self, count):
        bulk = []
        for i in range(1, count):
            me = {
                "username": f"test_user_{i}",
                "password": make_password(f"test_user_{i}")
            }
            bulk.append(User(**me))
        return User.objects.bulk_create(bulk)

    def handle(self, *args, **options):
        _len = options.get("len", self.RANGE)
        self.create_bulk_users(_len)
