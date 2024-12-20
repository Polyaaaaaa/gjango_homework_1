from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Product, Category


# Create your views here.


class HomeView(ListView):
    model = Product


class ContactsView(TemplateView):
    model = Product
    template_name = 'catalog/contacts.html'


class ProductDetailView(DetailView):
    model = Product
