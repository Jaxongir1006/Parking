from django.apps import apps
from django.contrib.auth.models import BaseUserManager


class DriverManager(BaseUserManager):
    def get_queryset(self):
        CustomUser = apps.get_model('user', 'CustomUser')
        return super().get_queryset().filter(user_type=CustomUser.UserTypeEnum.DRIVER)

class AdminManager(BaseUserManager):
    def get_queryset(self):
        CustomUser = apps.get_model('user', 'CustomUser')
        return super().get_queryset().filter(user_type=CustomUser.UserTypeEnum.ADMIN)

class OwnerManager(BaseUserManager):
    def get_queryset(self):
        CustomUser = apps.get_model('user', 'CustomUser')
        return super().get_queryset().filter(user_type=CustomUser.UserTypeEnum.OWNER)
