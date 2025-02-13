# catalog/urls.py
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from catalog import views
from catalog.views import HomeView, ContactsView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductListView, ProductDeleteView, ProductListByCategoryView

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
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"), # URL для обновления продукта
    path('products/<int:pk>/unpublish/', ProductListView.as_view(), name='unpublish_product'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('category/<int:category_id>/', ProductListByCategoryView.as_view(), name='product_list_by_category'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
