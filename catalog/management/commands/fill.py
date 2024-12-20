from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import random


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми категориями и продуктами'

    def handle(self, *args, **kwargs):
        # Список тестовых данных
        categories_data = [
            {'name': 'Электроника', 'description': 'Товары из мира электроники'},
            {'name': 'Одежда', 'description': 'Модная одежда на любой вкус'},
            {'name': 'Книги', 'description': 'Книги разных жанров'},
        ]

        products_data = [
            {'name': 'Смартфон', 'description': 'Мощный смартфон с большим экраном'},
            {'name': 'Футболка', 'description': 'Качественная футболка из хлопка'},
            {'name': 'Роман', 'description': 'Интересный роман для вечеров'},
            {'name': 'Наушники', 'description': 'Беспроводные наушники с отличным звуком'},
            {'name': 'Джинсы', 'description': 'Стильные джинсы для повседневной носки'},
        ]

        # Удаление старых записей
        Category.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('Старые записи удалены.')

        # Создание категорий
        categories = {}
        for category_data in categories_data:
            category = Category.objects.create(**category_data)
            categories[category.name] = category
            self.stdout.write(f'Создана категория: {category.name}')

        # Создание продуктов
        for product_data in products_data:
            category = random.choice(list(categories.values()))
            product = Product.objects.create(
                **product_data,
                category=category,
                price=random.uniform(100, 1000)
            )
            self.stdout.write(f'Создан продукт: {product.name} в категории {category.name}')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))