from django.contrib import admin
from settings.models import *
# Register your models here.


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id','name']




@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id','country','name']



@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['id','brand','type']




@admin.register(Membership)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['id','package','is_pay','start_date','expire_date']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['id','name','is_active','default_price']