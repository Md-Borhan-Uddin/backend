from settings.models import *
from rest_framework import serializers
from realestate.models import AssertBrand, AssertType
from realestate.serializers import AssertBrandSerializers, AssertTypeSerializers
from accounts.serializers import UserSerializer


class CountrySerializer(serializers.ModelSerializer):


    class Meta:
        model = Country
        fields = '__all__'

    def validate_name(self, value):
        if self.instance is not None and self.instance.name == value:
            return value
        if Country.objects.filter(name=value).exists():
            raise serializers.ValidationError('City name already exists. Try another name.')
        return value
    
    def create(self, validated_data):
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    
class AssetSerializers(serializers.ModelSerializer):
    brand_id = serializers.IntegerField(write_only=True)
    type_id = serializers.IntegerField(write_only=True)
    type = AssertTypeSerializers(read_only=True)
    brand = AssertBrandSerializers(read_only=True)

    class Meta:
        model = Asset
        fields = ['id','brand','type','brand_id','type_id']
    
    
    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        c_id = validated_data.get('category_id')
        t_id = validated_data.get('type_id')
        type = AssertType.objects.get(id=t_id)
        cat = AssertBrand.objects.get(id=c_id)
        instance.category = cat
        instance.type = type
        instance.save()
        return instance



class CitySerializer(serializers.ModelSerializer):
    country_id = serializers.IntegerField(write_only=True)
    country = CountrySerializer(read_only=True)

    class Meta:
        model = City
        fields = ['id','name','country','country_id']


    def validate_name(self, value):
        if self.instance is not None and self.instance.name == value:
            return value
        if City.objects.filter(name=value).exists():
            raise serializers.ValidationError('City name already exists. Try another name.')
        return value

    def create(self, validated_data):
        return super().create(validated_data)
    
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        id = validated_data.get('country_id')
        country = Country.objects.get(id=id)
        instance.country = country
        instance.save()
        return instance






class PackageSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Package
        fields = ['id','name','description','feature', 'duration_date','duration_month','is_free','is_active','pricing_approach',
                  'default_price','default_real_estate_number','is_renewal','enabling_adding_extra_real_estate',
                  'price_per_real_estate','create','update'
                  ]


    def validate_name(self, value):
        if self.instance is not None and self.instance.name == value:
            return value
        if Package.objects.filter(name=value).exists():
            raise serializers.ValidationError('Package name already exist Try another name')
        return value

    def create(self, validated_data):
        package = Package.objects.create(**validated_data)
        return package

    def update(self, instance, validated_data):
        print("serializer",validated_data)
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.duration_date = validated_data.get('duration_date',instance.duration_date)
        instance.duration_month = validated_data.get('duration_month',instance.duration_month)
        instance.is_free = validated_data.get('is_free',instance.is_free)
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.pricing_approach = validated_data.get('pricing_approach',instance.pricing_approach)
        instance.default_real_estate_number = validated_data.get('default_real_estate_number',instance.default_real_estate_number)
        instance.default_price = validated_data.get('default_price',instance.default_price)
        instance.is_renewal = validated_data.get('is_renewal',instance.is_renewal)
        instance.enabling_adding_extra_real_estate = validated_data.get('enabling_adding_extra_real_estate',instance.enabling_adding_extra_real_estate)
        instance.price_per_real_estate = validated_data.get('price_per_real_estate',instance.price_per_real_estate)
        instance.feature = validated_data.get('feature',instance.feature)
        instance.save()
        return instance
    




class MembershipSerializer(serializers.ModelSerializer):
    package_id = serializers.IntegerField(write_only=True)
    package = PackageSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    # user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Membership
        fields = ['id','package','package_id','start_date','expire_date', 'is_pay','user']


    def validat(self, data):
        print(data.get('user'))
        request = self.context.get('request')
        pac = Package.objects.get(name=data.get('package_id'))
        user = User.objects.get(id=data)
        if Membership.objects.filter(user=user, is_active=True).exists():
            raise serializers.ValidationError(f'You have an active membership that expired on {data["expaire_date"]}, Would like cancel it, and proceed with new membership')
        return data

    def create(self, validated_data):
        package = Package.objects.get(id=validated_data.get('package_id'))
        # validated_data.pop('expire_date')
        # print(package)
        # expire_date = 
        request = self.context.get('request')
        print(request.user)
        return Membership.objects.create(user=request.user,**validated_data)
    
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        pac = Package.objects.get(name=validated_data.get('package_id'))
        
        instance.package = pac
        instance.save()
        return instance