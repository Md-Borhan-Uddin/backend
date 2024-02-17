from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserType(models.TextChoices):
    ADMIN = "Admin", "Admin"
    REALTOR = "RealTor", "RealTor"


class User(AbstractUser):
    middel_name = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    mobile_number = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\+[0-9]{3}[\s\./0-9]{10}$")],
    )

    user_type = models.CharField(max_length=10, choices=UserType.choices)
    is_realtor = models.BooleanField(default=False)
    image = models.ImageField(upload_to="profile", default="default.jpg")
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=UserType.ADMIN)


class Admin(User):
    class Meta:
        proxy = True

    objcets = AdminManager()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.user_type = UserType.ADMIN
            self.is_staff = True
            self.is_superuser = True
        return super().save(*args, **kwargs)


class RealTorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=UserType.REALTOR)


class RealTor(User):
    class Meta:
        proxy = True

    objects = RealTorManager()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.user_type = UserType.REALTOR
        return super().save(*args, **kwargs)


class RequestStatus(models.TextChoices):
    DEFAULT = "Default", "Default"
    APPROVE = "Approve", "Approve"
    REJECT = "Reject", "Reject"


class Visitor(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    mobile_number = PhoneNumberField()
    real_estate = models.ForeignKey("realestate.RealEstate", on_delete=models.CASCADE)
    is_aprove = models.CharField(
        max_length=10, choices=RequestStatus.choices, default=RequestStatus.DEFAULT
    )
    create = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.first_name


class Notification(models.Model):
    subject = models.CharField(max_length=250, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now=False, auto_now_add=True)
    to = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"notification for {self.to}"
