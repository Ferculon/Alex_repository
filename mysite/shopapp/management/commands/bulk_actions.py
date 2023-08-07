from django.contrib.auth.models import User

from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')

        # обновление данных об конкретном объекте с помощью update
        result = Product.objects.filter(name__contains='Smartphone',).update(discount=10)

        print(result)
        # info = [
        #     ('Smartphone One', 199),
        #     ('Smartphone Two', 299),
        #     ('Smartphone Three', 399),
        # ]
        #
        # products = [
        #     Product(name=name, price=price) for name, price in info
        # ]
        #
        # result = Product.objects.bulk_create(products)  # bulk_create позволяет создать несколько объектов из которых
        # # создаются новые записи в базе данных
        #
        # for obj in result:
        #     print(obj)

        self.stdout.write(self.style.SUCCESS("Done"))
