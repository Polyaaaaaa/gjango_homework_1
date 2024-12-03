from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'catalog/home.html')  # Представление для главной страницы


def contacts(request):
    return render(request, 'catalog/contacts.html')  # Представление для страницы контактов


