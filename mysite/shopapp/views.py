"""
В этом модуле лежат различные наборы представлений.

Разные view для интернет-магазина: по товарам, заказам и т.д.
"""
import logging
from csv import DictWriter

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from .common import save_csv_products
from .models import Product, Order, ProductImage
from .forms import ProductForm
from .serializers import ProductSerializer

from drf_spectacular.utils import extend_schema, OpenApiResponse

# создание логгера для логирования в разных местах конкретного модуля
# в логгинг нужно передавать не отформатированную строку, а правило, по которому будет идти форматирование
log = logging.getLogger(__name__)


# Чтобы документировать функции и классы и не пропуская параметры, то необходимо установить библиотеку
# flake8 командой pip install flake8. А затем установить расширение для этой библиотеки flake8docstrings
# командой pip install flake8-docstrings. А после заморозить зависимости: pip freeze > requirements.txt
# flake8 проверяет файлы на принадлежность стилю PEP8 командой flake8 приложение/файл.py
@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.
    Полный CRUD для сущностей товара.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    # поля поиска для SearchFilter
    search_fields = [
        'name',
        'descriptions',
    ]
    # поля поиска для DjangoFilterBackend
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]
    # поля поиска для OrderingFilter
    ordering_fields = [
        'name',
        'price',
        'discount',
    ]

    # настройка кэширования данных для конкретного метода в django REST
    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
    
    # с переопределением метода retrieve, extend_schema позволяет добавить описание в API приложении
    @extend_schema(
        summary='Get one product by ID',
        description='Retrieves **product**, returns 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response, product by ID not found'),
        },
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    # экспорт файлов из REST API
    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')  # подготовка объекта, в который будут выводиться данные
        filename = 'products_export.csv'
        # скачивание файла уже с готовым именем
        response['Content-Disposition'] = f'attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
               field: getattr(product, field) for field in fields
            })

        return response

    # загрузка файлов в REST API
    # Так как загрузка файла со страницы невозможна из-за того, что используется только метод post
    # в терминале пишется команда на уровне, где расположен файл для импорта:
    # curl -X POST -F 'название файла с расширением' (адрес на страницу импорта файлов в REST API)
    @action(methods=['post'], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


# вариант реализации списка товаров с помощью ListView (наследника TemplateView)
class ProductsListView(ListView):
    template_name = 'shopapp/products_list.html'
    # model = Product #указывается, если не указывается queryset
    context_object_name = 'products'  # имя, по которому будет доступен список продуктов
    queryset = Product.objects.filter(archived=False)


# вариант реализации списка продуктов с помощью View
# class ProductsListView(View):
#
#     def get(self, request: HttpRequest) -> HttpResponse:
#         products = Product.objects.all()
#         context = {
#             'products': products,
#         }
#
#         return render(request, 'shopapp/products_list.html', context=context)


# вариант реализации списка продуктов с помощью TemplateView (наследник View)
# class ProductsListView(TemplateView):
#
#     template_name = 'shopapp/products_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.all()
#         return context

# вариант реализации списка товаров с помощью DetailView (наследника TemplateView)
class ProductDetailView(DetailView):
    template_name = 'shopapp/product_details.html'
    # model = Product  #указывается, если не указывается queryset
    context_object_name = 'product'
    queryset = Product.objects.prefetch_related('images').filter(archived=False)


# реализация деталей продукта с помощью View
# class ProductDetailView(View):
#
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         product = get_object_or_404(Product, pk=pk) #при отсутствии продукта будет ошибка 404, а не серверная ошибка
#         context = {
#             'product': product
#         }
#
#         return render(request, 'shopapp/product_details.html', context=context)


# реализация создания продукта с помощью CreateView (наследник ModelForm)
# миксин UserPassesTestMixin делает проверку есть ли разрешение у пользователя на создание продукта
class ProductCreateView(CreateView):
    # def test_func(self):
    #     return self.request.user.is_superuser  #проверка на суперюзера, так как только он может создавать продукт
    model = Product
    fields = 'name', 'price', 'discount', 'description', 'preview'
    success_url = reverse_lazy('shopapp:products_list')
    # есть вариант использовать form_class = 'название формы' вместо fields и тогда
    # не надо будет описывать поля в классе, что должны быть в шаблоне
    # при создании шаблона нужно указать имя МОДЕЛИ и суффикс _FORM


# реализация изменения (обновления) описания продукта с помощью UpdateView (наследник ModelForm)
class ProductUpdateView(UpdateView):
    model = Product
    # fields = 'name', 'price', 'discount', 'description', 'preview'
    form_class = ProductForm  # указывается, если создана форма в файле forms.py
    template_name_suffix = '_update_form'  # коррекция суффикса при создании шаблона

    def get_success_url(self):
        return reverse('shopapp:product_details', kwargs={'pk': self.object.pk})

    # обработка формы
    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):  # получение картинок из поля 'images' и сохранение в объект
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


# реализация удаления или сокрытия продукта с помощью DeleteView (наследник ModelForm)
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')
    # при создании шаблона нужно указать имя МОДЕЛИ и суффикс _CONFIRM_DELETE

    # реализация архивирования продукта (soft delete)
    def form_valid(self, form):  # метод для удаления в DeleteView
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


# вариант реализации списка заказов с помощью ListView (наследника TemplateView)
# Миксин LoginRequiredMixin должен быть первым так как проверяет пользователя на право просматривать страницу. Если он
# не аутентифицирован, то доступ запрещен.
class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects.select_related('user').prefetch_related('products'))
    # при таком наборе параметров, шаблон должен называться именем МОДЕЛИ и с суффиком _LIST
    # обращение к списку заказов идет через OBJECT_LIST, если не указывать context_object_name


# вариант реализации списка заказов с помощью View
# class OrdersListView(View):
#
#     def get(self, request: HttpRequest) -> HttpResponse:
#         orders = Order.objects.select_related('user').prefetch_related('products')
#         context = {
#             'orders': orders
#         }
#         return render(request, 'shopapp/order_list.html', context=context)


# вариант реализации деталей заказа с помощью DetailView (наследника TemplateView)
# миксин PermissionRequiredMixin проверяет пользователя на конкретные разрешения (permission_required)
# если нет доступа, то выскочит ошибка 403 forbidden
class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order',  # проверка на возможность посмотреть детали заказа. Разрешения можно
    # перечислить в списке или через запятую
    queryset = (Order.objects.select_related('user').prefetch_related('products'))
    # при таком наборе параметров, шаблон должен называться именем МОДЕЛИ и с суффиком _DETAIL
    # обращение к списку заказов идет через OBJECT, если не указывать context_object_name


# вариант создания списка продуктов в виде функции
# def products_list(request: HttpRequest):
#     products = Product.objects.all()
#
#     context = {
#         'products': products
#     }
#     return render(request, 'shopapp/products_list.html', context=context)


# вариант создания продукта с помощью функции
# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             # Product.objects.create(**form.cleaned_data) #когда в форме нет класса Meta и не использована модель
#             form.save()
#             url = reverse('shopapp:products_list')
#             return redirect(url)
#     else:
#         form = ProductForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'shopapp/create_product.html', context=context)


# Выгрузка данных из базы данных и возвращены как JSON - объект
class ProductsDataExportView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        cache_key = 'products_data_export'
        # получение данных из кэша по ключу
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by('pk').all()
            products_data = [
                {
                    'pk': product.pk,
                    'name': product.name,
                    'price': product.price,
                    'archived': product.archived,
                }
                for product in products
            ]
            # установка кэша, чтобы положить в него данные .set(ключ, данные, срок для кэша)
            cache.set(cache_key, products_data, 300)
        return JsonResponse({'products': products_data})
