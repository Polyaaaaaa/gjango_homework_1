# catalog/urls.py
from django.urls import path
from catalog.views import home, contacts, product_detail
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),  # URL для главной страницы
    path('contacts/', contacts, name='contacts'),  # URL для страницы контактов
    path('products/<int:pk>/', product_detail, name='product_detail'),  # URL для деталей продукта
]
