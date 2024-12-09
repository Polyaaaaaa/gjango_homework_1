import os

from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html')  # Представление для главной страницы


def contacts(request):
    return render(request, 'contacts.html')  # Представление для страницы контактов


