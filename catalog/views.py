from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)
from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Category
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from catalog.services import ProductService


class ProductListByCategoryView(ListView):
    model = Product
    template_name = 'catalog/product_list_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Получаем идентификатор категории из URL
        category_id = self.kwargs['category_id']

        # Используем сервис для получения списка продуктов в категории
        return ProductService.get_product_list(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем объект категории
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)

        # Добавляем категорию в контекст
        context['category'] = category
        return context


class HomeView(ListView):
    model = Product


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.object.id
        context['product_list'] = ProductService.get_product_list(product_id)
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy("products:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("products:product_detail", args=[self.object.pk])


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

    def form_valid(self, form):
        # Проверяем, является ли пользователь модератором
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return super().form_valid(form)
        # Если пользователь не модератор, удаляем поле 'status' из данных формы
        form.cleaned_data.pop('status', None)
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_delete'] = self.request.user.has_perm('catalog.delete_product')
        return context

    def get_queryset(self):
        # Получаем кешированный queryset
        queryset = cache.get('products_queryset')

        if not queryset:
            # Если кеш пуст, создаем новый queryset
            queryset = super().get_queryset()

            # Проверка прав доступа
            if not (self.request.user.is_staff or self.request.user.has_perm("catalog.view_all_products")):
                queryset = queryset.filter(owner=self.request.user)

            # Кешируем queryset
            cache.set('products_queryset', queryset, 60 * 15)

        return queryset


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
