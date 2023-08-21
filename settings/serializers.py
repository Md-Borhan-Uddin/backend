from settings.models import *
from rest_framework import serializers
from realestate.models import AssertBrand, AssertType
from realestate.serializers import AssertBrandSerializers, AssertTypeSerializers
from accounts.serializers import UserSerializer


class CountrySerializer(serializers.ModelSerializer):


    class Meta:
        model = Country
        fields = ['id','name','is_active','create','update']

    
    def create(self, validated_data):
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
    
class AssetSerializers(serializers.ModelSerializer):
    

    class Meta:
        model = Asset
        fields = ['id','brand','type']
    
    
    def create(self, validated_data):

        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)



class CitySerializer(serializers.ModelSerializer):
    country_id = serializers.IntegerField(write_only=True)
    country = CountrySerializer(read_only=True)

    class Meta:
        model = City
        fields = ['id','name','country','country_id','is_active']



    def create(self, validated_data):
        return super().create(validated_data)
    
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        id = validated_data.get('country_id')
        if id:
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


   

    def create(self, validated_data):
        package = Package.objects.create(**validated_data)
        return package

    def update(self, instance, validated_data):
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

    class Meta:
        model = Membership
        fields = ['id','package','package_id','start_date','expire_date', 'is_pay','user']


    def validate(self, data):
        
        request = self.context.get('request')
        # pac = Package.objects.get(name=data.get('package_id'))
        user = request.user
        if Membership.objects.filter(user=user, is_active=True).exists():
            raise serializers.ValidationError(f'You have an active membership that expired on {data["expire_date"]}, Would like cancel it, and proceed with new membership')
        return data

    def create(self, validated_data):
        
        request = self.context.get('request')
        package_id = validated_data.pop('package_id')
        package = Package.objects.get(pk=package_id)
        
        return Membership.objects.create(user=request.user,package=package,**validated_data)
    
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        pac = Package.objects.get(name=validated_data.get('package_id'))
        
        instance.package = pac
        instance.save()
        return instance