from .models import Product, Category


class ProductService:

    @staticmethod
    def get_full_name(product_id):
        products = Product.objects.get(id=product_id)
        return f"{products.name}"

