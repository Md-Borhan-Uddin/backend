from rest_framework import serializers
from accounts.models import User, RealTor,Admin
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber
from djoser.serializers import UserCreateSerializer
# from settings.serializers import PackageSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView





class UserSerializer(serializers.ModelSerializer):
    # package = PackageSerializer()
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','image','middel_name','user_type','email','mobile_number','is_active', 'date_joined']



class UserEditSerializer(serializers.ModelSerializer):
    mobile_number = PhoneNumberField(region='SA')
    class Meta:
        model = User
        fields = ['username','first_name','last_name','image','middel_name','email','mobile_number', 'is_active']

    def update(self,instance, validated_data):
        print(validated_data)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middel_name = validated_data.get('middel_name', instance.middel_name)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.image = validated_data.get('image',instance.image)

        instance.save()
        return instance





class UserCreateSerializer(UserCreateSerializer):
    mobile_number = PhoneNumberField(region='BD')
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['username','password','password2','first_name','last_name','middel_name','email','mobile_number', 'date_joined']

    def update(self,instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middel_name = validated_data.get('middel_name', instance.middel_name)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)

        instance.save()
        return instance


    def validate_username(self, value):
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(detail={"message":"Username Already Exist Please try another"})
        return value

    def validate_email(self, value):
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(detail={"message":"Email Already Exist Please try another"})
        return value

    def validate_mobile_number(self, value):
        
        
        if User.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError(detail={"message":"Mobile NUmber Already Exist Please try another"})
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(detail={"message":"Username Already Exist Please try another"})
        return value

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError(detail={'message':'Password Don\'t match'})
        return data

    def create(self, validated_data):
        
        password2 = validated_data.pop('password2')
        

        return User.objects.create_user(**validated_data)



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(
        style={'input_type':'password'}, max_length=20,
        
        )
    # class Meta:
    #     fields = ['username', 'password']

class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        style={'input_type':'password'}, max_length=20,
        
    )
    
    confirm_password = serializers.CharField(
        style={'input_type':'password'}, max_length=20,
        
    )

    def validate(self, data):
        confirm_password = data.get('confirm_password')
        confirm_password = data.get('confirm_password')
        if confirm_password != confirm_password:
            raise serializers.ValidationError(detail={'message':'Password Don\'t match'})
        return data

    


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

