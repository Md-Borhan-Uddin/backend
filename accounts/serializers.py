from rest_framework import serializers

from accounts.models import Notification, User, Visitor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "image",
            "middel_name",
            "user_type",
            "email",
            "mobile_number",
            "is_active",
        ]


class UserEditSerializer(serializers.ModelSerializer):
    # middel_name = serializers.CharField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "image",
            "middel_name",
            "email",
            "mobile_number",
            "user_type",
            "is_active",
        ]

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            setattr(instance, key, val)
        # instance.first_name = validated_data.get('first_name', instance.first_name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.middel_name = validated_data.get('middel_name', instance.middel_name)
        # instance.email = validated_data.get('email', instance.email)
        # instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        # instance.is_active = validated_data.get('is_active', instance.is_active)
        # instance.image = validated_data.get('image',instance.image)

        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
            "first_name",
            "last_name",
            "middel_name",
            "email",
            "mobile_number",
            "date_joined",
        ]

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            setattr(instance, key, val)
        # instance.first_name = validated_data.get('first_name', instance.first_name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.middel_name = validated_data.get('middel_name', instance.middel_name)
        # instance.email = validated_data.get('email', instance.email)
        # instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)

        instance.save()
        return instance

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                detail={"message": "Password Don't match"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password2")

        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(
        style={"input_type": "password"},
        max_length=20,
    )
    # class Meta:
    #     fields = ['username', 'password']


class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        style={"input_type": "password"},
        max_length=20,
    )

    confirm_password = serializers.CharField(
        style={"input_type": "password"},
        max_length=20,
    )

    def validate(self, data):
        confirm_password = data.get("confirm_password")
        confirm_password = data.get("confirm_password")
        if confirm_password != confirm_password:
            raise serializers.ValidationError(
                detail={"message": "Password Don't match"}
            )
        return data


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, attrs):
        real_estate_id = attrs.get("real_estate")
        if Visitor.objects.filter(real_estate=real_estate_id).exists():
            raise serializers.ValidationError("already requested")
        return attrs
