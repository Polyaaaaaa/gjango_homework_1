# from django.shortcuts import render
# from django.views import View
from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)

from catalog.forms import ProductForm
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
    success_url = reverse_lazy("products:product_list")


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(publication_sign=True)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("products:product_list")

    def get_success_url(self):
        return reverse("products:product_detail", args=[self.kwargs.get("pk")])
