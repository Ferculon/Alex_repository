from random import choices
from string import ascii_letters

from django.conf import settings
from django.contrib.auth.models import User

from .views import Product

from django.test import TestCase
from django.urls import reverse


#тест на создание сущности (создание продукта)
class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None: #настройка теста, которая происходит перед его началом
        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete() #проверка на наличие названия продукта в таблице и,
        # если таково есть, то продукт удаляется

    def test_product_create(self):
        response = self.client.post(
            reverse('shopapp:create_product'),
            {
                'name': self.product_name,
                'price': '123.45',
                'discount': '10',
                'description': 'A good table',
            },
            HTTP_USER_AGENT='Mozilla/5.0',
        )
        self.assertRedirects(response, reverse('shopapp:products_list')) #проверка, действительно ли идет перенаправление
        #после создания сущности на конкретную страницу
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists(),
        ) #проверка, действительно ли теперь есть такой продукт в таблице


#проверка деталей продукта
class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls): #настройка, которая гарантирует, что сущность будет создана один раз
        cls.product = Product.objects.create(name='Best Product')

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()


    # def setUp(self) -> None:
    #     self.product = Product.objects.create(name='Best Product')
    #
    # #позволяет почистить базу от объектов, которые были созданы для проверки и выполняется в любом случае независимо от
    # #результата теста.
    # def tearDown(self) -> None:
    #     self.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk}),
            HTTP_USER_AGENT='Mozilla/5.0',
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self): #проверяет содержимое страницы
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk}),
            HTTP_USER_AGENT='Mozilla/5.0',
        )
        self.assertContains(response, self.product.name)

#чтобы выгрузить данные из базы данных в файл, выполняется команда:
# python manage.py dumpdata 'название приложения' > 'название приложения'-fixtures.json

#чтобы загрузить данные в базу данных из файла, выполняется команда:
# python manage.py loaddata 'название приложения'-fixtures.json


#проверка на наличие неархивированных продуктов
class ProductsListViewTestCase(TestCase):

    fixtures = [
        'products-fixture.json',
    ]

    def test_products_list(self):
        response = self.client.get(reverse('shopapp:products_list'), HTTP_USER_AGENT='Mozilla/5.0',)
        # for product in Product.objects.filter(archived=False).all(): #проверка по имени продукта
        #     self.assertContains(response, product.name)

        # products = Product.objects.filter(archived=False).all() #взяты сущности из базы
        # products_ = response.context['products'] #взят контекст из ответа. .context['products'] потому что в
        # context_object_name указан 'products' в ProductsListView
        # for p, p_ in zip(products, products_): #сравнение по id продуктам
        #     self.assertEqual(p.pk, p_.pk)

        # прямая проверка по Queryset. Значения: qs - сам Queryset, values - значения из контекста
        # с которыми надо сравнить, transform - как преобразовывать объекты, чтобы сравнить с values.
        # Значения в transform и в values должны быть одинаковыми
        # Так как Queryset не имеет порядка, а в values он есть, то в избежании ошибки используется ordered со значением
        # False
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context['products']),
            transform=lambda p: p.pk,
            ordered=False,
        )
        self.assertTemplateUsed(response, 'shopapp/products_list.html') # проверка шаблона, где используются данные


# проверка на наличие списка заказов
class OrdersListViewTestCase(TestCase):

    # настройка аутентификации для одного пользователя
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='Alex', password='12345')  # данные пользователя в отдельной переменной
        cls.user = User.objects.create_user(**cls.credentials)  # создание пользователя с распаковкой данных

    # удаление созданного пользователя после теста
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    # аутентификация созданного пользователя с распаковкой его данных
    def setUp(self) -> None:
        # self.client.login(**self.credentials)
        self.client.force_login(self.user)  # принудительная аутентификация без необходимости использовать распаковку данных

    def test_orders_list(self):
        response = self.client.get(reverse('shopapp:orders_list'), HTTP_USER_AGENT='Mozilla/5.0',)
        self.assertContains(response, 'Orders')

    # тест для проверки на неаутентифицированного пользователя
    def test_orders_list_not_authenticated(self):
        self.client.logout()  # выход пользователя из под своей учетной записи
        response = self.client.get(reverse('shopapp:orders_list'), HTTP_USER_AGENT='Mozilla/5.0',)
        # self.assertRedirects(response, str(settings.LOGIN_URL))  # проверка на перенаправление для аутентификации

        # чтобы точно сравнить перенаправление и не получить ошибку, выполняется 2 проверки
        self.assertEqual(response.status_code, 302)  # проверка на статус код
        self.assertIn(str(settings.LOGIN_URL), response.url)  # проверка на то, входит ли строка с перенаправлением в
        # ответ response.url


# тест TDD (Test Driven Development)
#
class ProductsExportViewTestCase(TestCase):

    fixtures = [
        'products-fixture.json',
    ]

    # Данный тест проверяет на совпадение выгруженных данных с данными в базе данных
    def test_get_products_view(self):
        response = self.client.get(
            reverse('shopapp:products_export'), HTTP_USER_AGENT='Mozilla/5.0',
        )  # по адресу 'shopapp:products_export' необходимо будет добавить новую view - функцию.
        # Суть TDD: сначала определяем требования к тесту, затем идет их реализация

        self.assertEqual(response.status_code, 200)  # проверка на статус - код
        products = Product.objects.order_by('pk').all()  # выгружаем продукты из базы данных с сортировкой по 'pk'
        expected_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': str(product.price),
                'archived': product.archived
            }
            for product in products
        ]  # создание списка значений продукта для всех продуктов. 'Price' оборачиваем в строку, чтобы число было как строка

        products_data = response.json()  # получение json - тела
        self.assertEqual(products_data['products'], expected_data)  # проверка на схожесть загруженных данных и данных из базы
