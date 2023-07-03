from django.contrib import admin
from realestate.models import *
# Register your models here.


@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ['id','realestate_id','name']


@admin.register(Assert)
class AssertAdmin(admin.ModelAdmin):
    list_display = ['id','name']


@admin.register(RealEstateType)
class RealEstateTypeAdmin(admin.ModelAdmin):
    list_display = ['id','name']


@admin.register(AssertType)
class AssertTypeadmin(admin.ModelAdmin):
    list_display = ['id','name']



@admin.register(AssertBrand)
class AssertTypeadmin(admin.ModelAdmin):
    list_display = ['id','name']



@admin.register(ScheduleMaintaines)
class ScheduleMaintainesadmin(admin.ModelAdmin):
    list_display = ['id','name']