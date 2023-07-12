from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator
# Create your models here.

class UserType(models.TextChoices):
    ADMIN = 'Admin','Admin'
    REALTOR = 'RealTor','RealTor'

class User(AbstractUser):
    
    middel_name = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=254)
    mobile_number = PhoneNumberField(region='SA')

    user_type = models.CharField(max_length=10, choices=UserType.choices)
    is_realtor = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile', default='default.jpg')

class AdminManager(models.Manager):
    def  get_queryset(self):
        return super().get_queryset().filter(user_type=UserType.ADMIN)




class Admin(User):


    class Meta:
        proxy = True

    objcets = AdminManager()
    def save(self,*args, **kwargs):
        if self.pk is None:
            self.user_type = UserType.ADMIN
            self.is_staff = True
            self.is_superuser = True
        return super().save(*args, **kwargs)



class RealTorManager(models.Manager):
    def  get_queryset(self):
        return super().get_queryset().filter(user_type=UserType.REALTOR)


class RealTor(User):


    class Meta:
        proxy = True

    objects = RealTorManager()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.user_type = UserType.REALTOR
        return super().save(*args, **kwargs)







class Notification(models.Model):
    subject = models.CharField(max_length=250, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now=False, auto_now_add=True)
    to = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'notification for {self.to}'
    