from datetime import datetime


from django.db import models

from accounts.models import User

# Create your models here.


class AbstractCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RealEstateType(AbstractCategory):
    def __str__(self):
        return self.name


class RealEstate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    realestate_id = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="realEstate/image")
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.JSONField(default=dict)
    type = models.ForeignKey(RealEstateType, on_delete=models.CASCADE)
    property_age_years = models.CharField(max_length=3)
    property_age_months = models.IntegerField()
    authorized = models.CharField(max_length=20, blank=True, default="")
    purchasing_cost = models.DecimalField(max_digits=10, decimal_places=2)
    cost_currency = models.CharField(max_length=50)
    cost_date = models.DateField(auto_now=False, auto_now_add=False)
    purpose = models.CharField(max_length=50)
    number_of_floors = models.CharField(max_length=4, null=True, blank=True)
    invoice_file = models.FileField(upload_to="realestate/file", null=True, blank=True)
    create = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        date = datetime.now().date().strftime("%Y%m%d")
        r = RealEstate.objects.last()
        id = 0
        if r:
            id = r.id

        self.realestate_id = date + str(id + 1)
        return super().save()


class AssertType(AbstractCategory):
    def __str__(self):
        return self.name


class AssertBrand(AbstractCategory):
    category = models.ForeignKey(AssertType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Assert(models.Model):
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="assert/image")
    type = models.ForeignKey(AssertType, on_delete=models.CASCADE)
    brand = models.ForeignKey(AssertBrand, on_delete=models.CASCADE)
    model = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    quantity = models.IntegerField()
    purchasing_price = models.DecimalField(max_digits=20, decimal_places=2)
    purchasing_currency = models.CharField(max_length=100)
    purchasing_date = models.DateField(auto_now=False, auto_now_add=False)
    floor_name = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)
    assert_file = models.FileField(null=True, blank=True, upload_to="assert/file")

    def __str__(self):
        return self.name


class ScheduleMaintainsStatue(models.TextChoices):
    ACTIVE = "Active", "Active"
    CANCELE = "Cancele", "Cancele"
    DONE = "Done", "Done"


class ScheduleMaintains(models.Model):
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    asset = models.ForeignKey(Assert, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    maintain_date = models.DateField(auto_now=False, auto_now_add=False)
    reminder_date = models.DateField(auto_now=False, auto_now_add=False)
    is_reminder = models.BooleanField(default=False)
    status = models.CharField(
        max_length=30,
        choices=ScheduleMaintainsStatue.choices,
        default=ScheduleMaintainsStatue.ACTIVE,
    )
    related_invoice = models.FileField(
        upload_to="schedule-invoice", blank=True, null=True
    )
    create = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name
