# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # URL для главной страницы
    path('contacts/', views.contacts, name='contacts'),  # URL для страницы контактов
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),  # URL для деталей продукта
]
