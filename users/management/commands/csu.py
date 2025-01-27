from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product  # Убедитесь, что путь к модели правильный


class Command(BaseCommand):
    help = 'Создать группу "Модератор продуктов" и назначить права'

    def handle(self, *args, **kwargs):
        group_name = "Модератор продуктов"

        # Создание группы, если она не существует
        group, created = Group.objects.get_or_create(name=group_name)

        # Получение разрешений
        permissions = [
            "can_unpublish_product",
            "can_delete_product",
        ]

        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)

        group.save()
        self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана и права назначены.'))