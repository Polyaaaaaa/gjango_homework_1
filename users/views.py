# users\views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm


# Create your views here.
class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('products:home')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    # success_url = reverse_lazy('products:home')  # Перенаправление после успешного входа


class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = reverse_lazy('users:register')  # Перенаправление на страницу регистрации после выхода
