from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer

from .models import (
    Assert,
    AssertBrand,
    AssertType,
    RealEstate,
    RealEstateType,
    ScheduleMaintaines,
)


class RealEstateTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RealEstateType
        fields = ["id", "name", "is_active"]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.is_active = validated_data.get("is_active", instance.is_active)

        instance.save()
        return instance


class AssertBrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = AssertBrand
        fields = ["id", "name", "is_active"]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance


class AssertTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = AssertType
        fields = ["id", "name", "is_active"]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            setattr(instance, key, val)
        # instance.name = validated_data.get("name", instance.name)
        # instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance


class RealEstateSerializer(serializers.ModelSerializer):
    type_id = serializers.IntegerField(write_only=True)
    type = RealEstateTypeSerializers(read_only=True)
    user_id = serializers.CharField(write_only=True, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = RealEstate
        fields = [
            "id",
            "realestate_id",
            "user",
            "name",
            "photo",
            "country",
            "city",
            "type_id",
            "user_id",
            "type",
            "property_age_years",
            "property_age_months",
            "rented",
            "owner",
            "purchasing_cost",
            "cost_currency",
            "cost_date",
            "purpose",
            "location",
            "number_of_floors",
            "invoice_file",
            "create",
            "update",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        id = validated_data.pop("type_id")
        u_id = validated_data.get("user_id")

        u = None
        if u_id:
            validated_data.pop("user_id")
            u = User.objects.get(id=int(u_id))
        else:
            u = request.user
        typeobj = RealEstateType.objects.get(id=id)
        obj = RealEstate(**validated_data)
        obj.type = typeobj

        obj.user = u
        obj.save()

        return obj

    def update(self, instance, validated_data):
        request = self.context.get("request")
        type_id = validated_data.pop("type_id")
        u_id = validated_data.get("user_id")

        u = None
        if u_id:
            validated_data.pop("user_id")
            u = User.objects.get(id=int(u_id))
        else:
            u = request.user
        typeobj = RealEstateType.objects.get(id=type_id)

        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.type = typeobj
        instance.user = validated_data.get(u, instance.user)

        # instance.realestate_id = validated_data.get(
        #     "realestate_id", instance.realestate_id
        # )
        # instance.name = validated_data.get("name", instance.name)
        # instance.photo = validated_data.get("photo", instance.photo)
        # instance.country = validated_data.get("country", instance.country)
        # instance.city = validated_data.get("city", instance.city)
        # instance.type = validated_data.get("type", instance.type)
        # instance.property_age_years = validated_data.get("city", instance.city)
        # instance.property_age_months = validated_data.get(
        #     "property_age_months", instance.property_age_months
        # )
        # instance.rented = validated_data.get("rented", instance.rented)
        # instance.owner = validated_data.get("owner", instance.owner)
        # instance.purchasing_cost = validated_data.get(
        #     "purchasing_cost", instance.purchasing_cost
        # )
        # instance.cost_currency = validated_data.get(
        #     "cost_currency", instance.cost_currency
        # )
        # instance.cost_date = validated_data.get("cost_date", instance.cost_date)
        # instance.purpose = validated_data.get("purpose", instance.purpose)
        # instance.location = validated_data.get("location", instance.location)
        # instance.number_of_floors = validated_data.get(
        #     "number_of_floors", instance.number_of_floors
        # )
        # instance.invoice_file = validated_data.get(
        #     "invoice_file", instance.invoice_file
        # )
        instance.save()

        return instance


class RealEstateUpdateSerializer(serializers.ModelSerializer):
    type_id = serializers.IntegerField(write_only=True, required=False)
    type = RealEstateTypeSerializers(read_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = RealEstate
        fields = [
            "id",
            "realestate_id",
            "name",
            "photo",
            "country",
            "city",
            "type_id",
            "user_id",
            "user",
            "type",
            "property_age_years",
            "property_age_months",
            "rented",
            "owner",
            "purchasing_cost",
            "cost_currency",
            "cost_date",
            "purpose",
            "number_of_floors",
            "invoice_file",
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")
        id = validated_data.get("type_id")
        u_id = validated_data.get("user_id")

        u = None
        if u_id:
            validated_data.pop("user_id")
            u = User.objects.get(id=int(u_id))
        else:
            u = request.user
        typeobj = instance.type
        if not id:
            typeobj = RealEstateType.objects.get(id=id)

        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.type = typeobj
        instance.user = u

        # instance.name = validated_data.get("name", instance.name)
        # instance.photo = validated_data.get("photo", instance.photo.url)
        # instance.country = validated_data.get("country", instance.country)
        # instance.city = validated_data.get("city", instance.city)
        # instance.property_age_years = validated_data.get(
        #     "property_age_years", instance.property_age_years
        # )
        # instance.property_age_months = validated_data.get(
        #     "property_age_months", instance.property_age_months
        # )
        # instance.rented = validated_data.get("rented", instance.rented)
        # instance.owner = validated_data.get("owner", instance.owner)
        # instance.purchasing_cost = validated_data.get(
        #     "purchasing_cost", instance.purchasing_cost
        # )
        # instance.cost_currency = validated_data.get(
        #     "cost_currency", instance.cost_currency
        # )
        # instance.cost_date = validated_data.get("cost_date", instance.cost_date)
        # instance.purpose = validated_data.get("purpose", instance.purpose)
        # instance.number_of_floors = validated_data.get(
        #     "number_of_floors", instance.number_of_floors
        # )
        # instance.invoice_file = validated_data.get(
        #     "invoice_file", instance.invoice_file
        # )

        instance.save()
        return instance


class AssertSerializer(serializers.ModelSerializer):
    # real_estate = RealEstateSerializer()
    class Meta:
        model = Assert
        fields = [
            "id",
            "name",
            "brand",
            "type",
            "real_estate",
            "photo",
            "model",
            "description",
            "quantity",
            "purchasing_price",
            "purchasing_currency",
            "purchasing_date",
            "floor_name",
            "room_name",
            "assert_file",
        ]

    # def create(self, validated_data):
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)


class ScheduleMaintainesSerializer(serializers.ModelSerializer):
    real_estate = RealEstateSerializer(read_only=True)
    asset = AssertSerializer(read_only=True)
    real_estate_id = serializers.IntegerField(write_only=True)
    asset_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ScheduleMaintaines
        fields = "__all__"

    # def create(self, validated_data):
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)
