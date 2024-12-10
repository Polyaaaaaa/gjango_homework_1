from django.core.management.base import BaseCommand
from catalog.models import Product


class Command(BaseCommand):
    help = 'Add test products to the database'

    def handle(self, *args, **kwargs):
        product, _ = Product.objects.get_or_create(name='Test_name', category='Test_category')

        categories = [
            {'title': 'test', 'publication_date': '1904-01-01', 'product_name': product},
            {'title': 'test', 'publication_date': '1901-01-01', 'product_name': product},
        ]

        for product_data in categories:
            book, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added book: {product.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Book already exists: {product.title}'))