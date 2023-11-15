from django.contrib.auth.models import User
from django.core.management import BaseCommand
from typing import Sequence
from shopapp.models import Product, Order



class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')
        users = User.objects.values_list('username', flat=True)
        for user in users:
            print(user)
        print(list(users))
        # products_values = Product.objects.values('pk', 'name')
        # for p_values in products_values:
        #     print(p_values)

        self.stdout.write(f'DONE')

