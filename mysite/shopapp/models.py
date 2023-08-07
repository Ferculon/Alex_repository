from django.contrib.auth.models import User
from django.db import models


# данная функция генерирует путь с помощью объекта (instance), над которым происходит взаимодействие, и имени файла
def preview_product_directory_path(instance: 'Product', filename: str) -> str:
    return 'products/product_{pk}/preview/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    """
    Модель Product представляет товар,
    который можно продавать в интернет-магазине.

    Заказы тут: :model:`shopapp.Order`
    """
    # db_index позволяет ускорить поиск данных и дает прирост производительности
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=preview_product_directory_path)
    # фото продукта, которое будет отображаться как product.preview
    # в upload_to указывается путь откуда берется фото. Сюда можно передать не только строку, но и функцию, которая
    # будет генерировать путь к фото

    # чтобы работать с медиа файлами, потребуется установка отдельной библиотеки pillow (pip install pillow)
    # затем замораживаем зависимость (pip freeze > requirements.txt), чтобы в файле зависимостей (requirements.txt)
    # указать еще одну зависимость

    # @property
    # def description_short(self) -> str:
    #     if len(self.description) > 48:
    #         return self.description[:48] + '...'
    #     return self.description
    #
    # def __str__(self) -> str:
    #     return f'Product(pk={self.pk} name={self.name!r})'


# функция, которая генерирует путь до картинок
def product_images_directory_path(instance: 'ProductImage', filename: str) -> str:
    return 'products/product_{pk}/images/{filename}'.format(
        pk=instance.product.pk,
        filename=filename,
    )


# класс, который будет связан с моделью Product, чтобы дать возможность загружать несколько картинок к одному продукту
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders')
    receipt = models.FileField(null=True, upload_to='orders/receipts/')  # система сюда будет загружать чек
    # null=True указывает на то, что есть заказы, у которых нет чека и не у всех заказов будет чек, так как если заказ
    # только что создан, то чека у него быть не может. upload_to указывает папку куда будет сохраняться чек. Путь
    # основан на MEDIA_ROOT, а что прописывается в upload_to - это продолжение основного пути




