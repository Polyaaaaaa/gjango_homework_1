from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)
from catalog.forms import ProductForm, ProductModeratorForm, CustomUserCreationForm
from catalog.models import Product


class HomeView(ListView):
    model = Product


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("products:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse("products:product_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        # Если пользователь - владелец продукта
        if user == self.get_object().owner:
            return ProductForm
        # Если пользователь - модератор
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied('Извините, но вы не обладаете достаточным количеством прав.')

    def test_func(self):
        # Получаем объект продукта
        product = self.get_object()
        # Можно редактировать продукт, если пользователь - владелец или модератор
        return self.request.user == product.owner or self.request.user.has_perm("catalog.can_unpublish_product")


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_delete'] = self.request.user.has_perm('catalog.delete_product')
        return context

    def get_queryset(self):
        user = self.request.user
        # Проверка прав доступа
        if self.request.user.is_staff or self.request.user.has_perm("catalog.view_all_products"):
            return super().get_queryset()
        return super().get_queryset().filter(owner=user)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy('products:home')

    def test_func(self):
        product = self.get_object()
        # Проверяем, является ли пользователь владельцем продукта или имеет ли он право на удаление
        return self.request.user == product.owner or self.request.user.has_perm("catalog.can_delete_product")

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        # Проверяем права доступа
        if not self.test_func():
            return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")

        # Если права доступа есть, продолжаем с удалением
        return super().post(request, *args, **kwargs)
