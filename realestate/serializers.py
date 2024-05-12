from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer

from .models import (
    Assert,
    AssertBrand,
    AssertType,
    RealEstate,
    RealEstateType,
    ScheduleMaintains,
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
            "authorized",
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
            "authorized",
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
        instance.save()
        return instance


class AssertSerializer(serializers.ModelSerializer):
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


class ScheduleMaintainsSerializer(serializers.ModelSerializer):
    real_estate = RealEstateSerializer(read_only=True)
    asset = AssertSerializer(read_only=True)
    real_estate_id = serializers.IntegerField(write_only=True)
    asset_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ScheduleMaintains
        fields = "__all__"

    # def create(self, validated_data):
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)
