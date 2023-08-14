from django.contrib import admin
from .models import User, Notification, Visitor
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'to']



@admin.register(Visitor)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name']