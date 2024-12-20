from django.shortcuts import render
from catalog.models import Product
# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'object_list': products})


def contacts(request):
    return render(request, 'catalog/contacts.html')  # Представление для страницы контактов


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'catalog/product_detail.html', {'object_list': product})
