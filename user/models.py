from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import AdminManager, DriverManager, OwnerManager
from utils.models import ModelWithTimeStamp

class CustomUser(AbstractUser, ModelWithTimeStamp):
    class UserTypeEnum(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        DRIVER = 'driver', _('Driver')
        OWNER = 'owner', _('Owner')

    user_type = models.CharField(verbose_name=_("user_type"), max_length=100, choices=UserTypeEnum.choices,
                                 default=UserTypeEnum.DRIVER, blank=True)
    phone = models.CharField(verbose_name=_("phone"), max_length=20, blank=True, null=True)
    car_number = models.CharField(max_length=20,blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    @property
    def verify_email(self):
        self.email_verified = True
        self.save()

class Driver(CustomUser):
    objects = DriverManager()

    class Meta:
        proxy = True

class Admin(CustomUser):
    objects = AdminManager()

    class Meta:
        proxy = True

class Owner(CustomUser):
    objects = OwnerManager()

    class Meta:
        proxy = True

class Card(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    card_number = models.IntegerField()
    card_holder = models.CharField(max_length=100)
    expire_date = models.CharField(max_length=10)
