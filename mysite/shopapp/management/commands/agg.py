from django.contrib.auth.models import User
from django.core.management import BaseCommand
from typing import Sequence
from shopapp.models import Product, Order
from django.db.models import Avg, Max, Min, Count, Sum



class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(f'Start demo aggregate')

        # result = Product.objects.filter(name__icontains='Smartphone').aggregate(
        #     avarage_price=Avg('price'),
        #     max_price=Max('price'),
        #     min_price=Min('price'),
        #     count=Count('id'),
        # )
        orders = Order.objects.annotate(
            total=Sum('products__price'),
            products_count=Count('products'),
        )
        for order in orders:
            print(
                f'Order #{order.id}'
                f'with {order.products_count}'
                f'product sum {order.total}'
            )
        self.stdout.write(f'DONE')

