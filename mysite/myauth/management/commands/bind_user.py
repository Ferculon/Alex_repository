from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


# создание команды, которая создает группу с разрешениями и добавляет туда конкретного пользователя
class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(pk=2)  # выбор пользователя
        group, created = Group.objects.get_or_create(
            name='profile_manager',
        )  # создание группы и ее названия
        permission_profile = Permission.objects.get(
            codename='view_profile',
        )  # создание разрешения

        # добавление разрешения в группу
        group.permissions.add(permission_profile)

        # добавление пользователя в группу с разрешениями
        user.groups.add(group)

        # присваение пользователю конкретного разрешения
        # user.user_permissions.add(permission_profile)

        group.save()
        user.save()
