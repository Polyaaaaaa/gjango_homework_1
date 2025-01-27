from django.db import models

from config import settings
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="имя категории")
    description = models.CharField(
        max_length=150, verbose_name="описание категории", blank=True, null=True
    )

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name", "description"]


class Product(models.Model):
    PRODUCT_STATUS_CHOICES = [
        ('unpublished', 'Неопубликован'),
        ('published', 'Опубликован')
    ]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products", null=True,
                              blank=True)  # Разрешаем NULL
    name = models.CharField(max_length=150, verbose_name="Имя продукта")
    description = models.TextField(
        verbose_name="Описание продукта", null=True, blank=True
    )
    image = models.ImageField(
        verbose_name="Изображение", blank=True, null=True, upload_to="catalog/images/"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    price = models.FloatField(verbose_name="Стоимость", blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    status = models.CharField(
        max_length=12,
        choices=PRODUCT_STATUS_CHOICES,
        default='unpublished',
        verbose_name="Статус публикации"
    )

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name", "description", "category"]
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
            ("can_delete_product", "Can delete product"),
            ("view_all_products", "View all products"),
        ]
