# from django.shortcuts import render
# from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView, DeleteView,
)

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product


# Create your views here.


class HomeView(ListView):
    model = Product


class ContactsView(TemplateView):
    model = Product
    template_name = "catalog/contacts.html"


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("products:home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy("products:product_list")

    def get_success_url(self):
        return reverse("products:product_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product") and user.has_perm("catalog.can_delete_product"):
            return ProductModeratorForm
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_unpublish'] = self.request.user.has_perm('catalog.can_unpublish_product')
        context['can_delete'] = self.request.user.has_perm('catalog.can_delete_product')
        return context


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        # Допустим, только владелец или администратор видят свои товары
        user = self.request.user
        if user.is_staff or user.has_perm("catalog.view_all_products"):
            return queryset
        return queryset.filter(owner=user)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"  # Шаблон для подтверждения удаления
    context_object_name = "product"
    success_url = reverse_lazy('products:home')  # URL для перенаправления после успешного удаления

    def test_func(self):
        # Проверяем, имеет ли пользователь право удалять продукт
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        # Ограничиваем видимость продуктов только для владельца или администраторов
        user = self.request.user
        if user.is_staff or user.has_perm("catalog.view_all_products"):
            return queryset
        return queryset.filter(owner=user)
