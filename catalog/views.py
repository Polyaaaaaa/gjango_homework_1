from django.shortcuts import render

from catalog.models import Product


# Create your views here.
def home(request):
    return render(request, 'home.html')  # Представление для главной страницы


def contacts(request):
    return render(request, 'contacts.html')  # Представление для страницы контактов


def products_list(request):
    products = Product.objects.all()
    context = {'products': products}
    print(products)
    return render(request, 'catalog/products_list.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)
