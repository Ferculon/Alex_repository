from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

from .views import (
    ProductsListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductsDataExportView,
    OrdersListView,
    OrderDetailView,
    ProductViewSet,
    )

app_name = 'shopapp'

routers = DefaultRouter()
routers.register('products', ProductViewSet)

urlpatterns = [
    path('api_products/', include(routers.urls)),
    path('products/', cache_page(60 * 3)(ProductsListView.as_view()), name='products_list'),
    path('products/create/', ProductCreateView.as_view(), name='create_product'),
    path('products/export/', ProductsDataExportView.as_view(), name='products_export'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name='archive_product'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_details'),
]
