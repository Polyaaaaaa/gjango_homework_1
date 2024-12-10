from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='имя категории')
    description = models.CharField(max_length=150, verbose_name='описание категории', blank=True)

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name', 'description']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя продукта')
    description = models.TextField(verbose_name='Описание продукта', null=True, blank=True)
    image = models.ImageField(verbose_name='Изображение', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.FloatField(verbose_name='Стоимость', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name', 'description', 'category']
