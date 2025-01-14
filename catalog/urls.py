# catalog/urls.py
from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactsView, HomeView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),  # URL для главной страницы
    path(
        "contacts/", ContactsView.as_view(), name="contacts"
    ),  # URL для страницы контактов
    path(
        "products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"
    ),  # URL для деталей продукта
]
