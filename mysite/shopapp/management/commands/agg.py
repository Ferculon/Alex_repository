from django.contrib.auth.models import User

from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Avg, Max, Min, Count, Sum

from shopapp.models import Product, Order


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Start demo aggregate')

        orders = Order.objects.annotate(
            total=Sum('products__price', default=0),
            products_count=Count('products'),
        )

        for order in orders:
            print(f'Order: {order.id}. Total sum: {order.total}. Products count: {order.products_count}')

        # пример агрегации со средним, максимальным, минимальным значением параметра конкретного товара и общее
        # количество товаров (Count)
        # result = Product.objects.filter(name__contains='Smartphone').aggregate(
        #     Avg('price'),
        #     Max('price'),
        #     min_price=Min('price'),
        #     count=Count('id'),
        # )
        # print(result)
        self.stdout.write(self.style.SUCCESS("Done"))
