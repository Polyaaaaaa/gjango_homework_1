# services.py
from .models import Product, Category


class ProductService:

    @staticmethod
    def get_product_list(category_id):
        # Получаем все продукты в указанной категории
        products = Product.objects.filter(category_id=category_id)
        return products
