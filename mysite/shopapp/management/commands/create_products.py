from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        products_name = [
            'Laptop',
            'Desktop',
            'Smartphone',
        ]
        for product_name in products_name:
            product, created = Product.objects.get_or_create(name=product_name)
            self.stdout.write(f'Product {product.name} created "{created}"')

        self.stdout.write(self.style.SUCCESS('Products created'))

