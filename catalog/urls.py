# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # URL для главной страницы
    path('contacts/', views.contacts, name='contacts'),  # URL для страницы контактов
]
