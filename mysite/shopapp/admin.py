from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .common import save_csv_products
from .models import Product, Order, ProductImage
from .admin_mixin import ExportAsCSVMixin
from .forms import CSVImportForm


# класс для отображения заказов, связанных с продуктом
class OrderInLine(admin.StackedInline):
    model = Product.orders.through

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


class ProductImageInLine(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = 'shopapp/products_changelist.html'

    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInLine,
        ProductImageInLine,
    ]
    # list_display = 'pk', 'name', 'description', 'price', 'discount'
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived' #объявление полей модели в админке
    list_display_links = 'pk', 'name' #поля получают ссылки на детали объекта
    ordering = 'pk', 'name'  #сортировка по полям
    search_fields = 'name', 'description' #поиск по полям
    # Добавление подполей с полями объекта (fields) и описанием подполя, которые можно скрыть (classes:collapse),
    # а так же изменением расстояния в поле (classes:wide), и описанием поля ('description': описание)
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('collapse', 'wide',),
        }),
        ('Images', {
            'fields': ('preview',),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': "Extra options. Field 'archived' is soft delete.", #Описание поля
        })
    ]

    # если метод нужно использовать только в админской модели, то реализуем его в admin.py
    def description_short(self, obj: Product) -> str:
        if len(obj.description) > 48:
            return obj.description[:48] + '...'
        return obj.description

    def __str__(self) -> str:
        return f'Product(pk={self.pk} name={self.name!r})'

    # настройка импорта данных в django admin с помощью функций import_csv и get_urls
    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)

        # вариант с применением файла common.py, где отдельно описан импорт
        save_csv_products(
            file=form.files['csv_file'].file,
            encoding=request.encoding,
        )
        # csv_file = TextIOWrapper(
        #     form.files['csv_files'].file,
        #     encoding=request.encoding,
        # )
        # reader = DictReader(csv_file)
        #
        # products = [
        #     Product(**row) for row in reader
        # ]
        # Product.objects.bulk_create(products)  # добавление сразу нескольких объектов
        self.message_user(request, 'Data form CSV was imported')
        return redirect('..')  # возврат на страницу назад

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import_products_csv/',
                self.import_csv,
                name='import_products_csv',
            ),
        ]
        return new_urls + urls

# admin.site.register(Product,ProductAdmin)


# класс для отображения продуктов, связанных с заказом
class ProductInLine(admin.StackedInline):
    model = Order.products.through

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInLine,
    ]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    #чтобы подгрузить пользователей, используем этот метод
    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    #чтобы отобразить имя заказчика вместо username, пишем такой метод
    def user_verbose(self, obj: Order) -> str:
        if obj.user.first_name is not None:
            return obj.user.first_name
        return obj.user.username
