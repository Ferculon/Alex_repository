from django.contrib.auth.models import User

from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Product


class Command(BaseCommand):

    # данный декоратор используется для создания заказа и, если все хорошо, то заказ будет создан, в противном случае
    # ничего не произойдет
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')

        # параметр flat делает из кортежа список со значениями
        users_info = User.objects.values_list('username', flat=True)
        for i_user in users_info:
            print(i_user)

        product_values = Product.objects.values('pk', 'name')
        for p_values in product_values:
            print(p_values)

        self.stdout.write(self.style.SUCCESS("Done"))
