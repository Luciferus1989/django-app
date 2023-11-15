from django.contrib.auth.models import User
from django.core.management import BaseCommand
from typing import Sequence
from shopapp.models import Product, Order



class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo bulk actions')
        result = Product.objects.filter(
            name__icontains='Smartphone',
        ).update(discount=10)
        # info = [
        #     ('Smartphone01', 111),
        #     ('Smartphone02', 222),
        #     ('Smartphone03', 333),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        # result = Product.objects.bulk_create(products)
        # print([obj for obj in result])
        # print(result)


        self.stdout.write(f'DONE')

