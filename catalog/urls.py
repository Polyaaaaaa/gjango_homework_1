# catalog/urls.py
from django.urls import path
from catalog.views import HomeView, ContactsView, ProductDetailView, ProductCreateView, ProductUpdateView

# from catalog.apps import CatalogConfig

# app_name = CatalogConfig.name
app_name = "products"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),  # URL для главной страницы
    path(
        "contacts/", ContactsView.as_view(), name="contacts"
    ),  # URL для страницы контактов
    path(
        "products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"
    ),  # URL для деталей продукта
    path("product_create/", ProductCreateView.as_view(), name="product_form"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),  # URL для обновления продукта
]
