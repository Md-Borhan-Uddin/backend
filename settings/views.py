from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,RetrieveAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from rest_framework.exceptions import ValidationError

#own file import
from settings.models import *
from settings.serializers import *
from .tasks import notification




# Create your views here.


class CountryListCreateAPIView(ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer




class CountryRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()




class CityListCreateAPIView(ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer




class CityRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer




class AssetListCreateAPIView(ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializers




class AssetRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializers





class PackageListCreateAPIView(ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def get_queryset(self):
        return Package.objects.filter(is_active = True)

    



class PackageRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def get_queryset(self):
        return Package.objects.filter(is_active = True)


class PackageRetrieveAPIViewByName(RetrieveAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = 'name'

    def get_queryset(self):
        return Package.objects.filter(is_active = True)
    
    


class MembershipListCreateAPIView(ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


    def create(self, request, *args, **kwargs):
        
        serializer = MembershipSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            id = serializer.data.get('user_id')
            user = User.objects.get(id=2)
            if Membership.objects.filter(user=user, expire_date__gt=datetime.now()).exists():
                raise serializers.ValidationError(f'You have an active membership that expired on, Would like cancel it, and proceed with new membership')
        
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        notification()
        user = self.request.user
        if user.user_type == 'Admin':
            return Membership.objects.all()
        return Membership.objects.filter(user=user,is_pay=True,expire_date__gt=datetime.now())


class ActiveMembershipList(ListAPIView):
    queryset = Membership.object.active()
    serializer_class = MembershipSerializer


class InactiveMembershipList(ListAPIView):
    queryset = Membership.object.inactive()
    serializer_class = MembershipSerializer


class MembershipRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    


    # def get_queryset(self):
    #     user = self.request.user
    #     id = self.kwargs.get('pk')
    #     print(self.kwargs)
    #     return Membership.objects.filter(user=user,is_pay=True,expire_date__lt=datetime.now())
