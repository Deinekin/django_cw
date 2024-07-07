from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='just_user3@mail.ru', # admin@mail.ru for admin
            first_name='just_user3',
            last_name='just_user3',
            is_staff=False,
            is_superuser=False,

        )

        user.set_password('1')
        user.save()
