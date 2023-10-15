# from django.utils.timezone import datetime
from django.db import models
from django.db.models.query import QuerySet
from realestate.models import AssertBrand, AssertType
from accounts.models import User
from datetime import timedelta, datetime
# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Countries"




class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Cities"


class Asset(models.Model):
    brand = models.ForeignKey(AssertBrand, on_delete=models.CASCADE)
    type = models.ForeignKey(AssertType, on_delete=models.CASCADE)

    def __str__(self):
        return f'category :{self.brand.name} type :{self.type.name}'
    
    class Meta:
        unique_together = ('brand','type')




class Package(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    feature = models.JSONField(default=dict)
    duration_date = models.IntegerField()
    duration_month = models.IntegerField()
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    pricing_approach = models.CharField(max_length=200)
    default_price = models.DecimalField(decimal_places=2,max_digits=10)
    default_real_estate_number = models.IntegerField()
    is_renewal = models.BooleanField()
    enabling_adding_extra_real_estate = models.BooleanField()
    price_per_real_estate = models.CharField(max_length=4)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# class InactiveManager(models.Manager):
    
#     def get_queryset(self):
#         return super().get_queryset().filter(is_pay=True)


# class ActiveManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_pay=True)
    


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package')
    is_pay = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    expire_date = models.DateTimeField()

    def __str__(self):
        return self.package.name



    
    
    