from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Order, Product


class Command(BaseCommand):

    # данный декоратор используется для создания заказа и, если все хорошо, то заказ будет создан, в противном случае
    # ничего не произойдет
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Create order with products')
        user = User.objects.get(username='admin')
        # загрузка queryset продуктов
        # defer исключает поля для загрузки, переданные ему в качестве аргументов
        # products: Sequence[Product] = Product.objects.defer('description', 'price', 'created_at').all()

        # only добавляет нужные поля для загрузки, переданные ему в качестве аргументов
        products: Sequence[Product] = Product.objects.only('id', 'name').all()

        order, created = Order.objects.get_or_create(
            delivery_address='Ul Glebova d. 10',
            promocode='PROMO1',
            user=user
        )

        for product in products:
            order.products.add(product)

        order.save()
        self.stdout.write(self.style.SUCCESS(f'Order {order} created "{created}"'))
