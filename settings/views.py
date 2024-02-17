from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, response
from rest_framework.decorators import api_view

# own file import
from utils.hyperpay import hyperpay_request
from settings.models import Asset, Country, City, Membership, Package
from accounts.models import User, UserType
from settings.serializers import (
    AssetSerializers,
    CitySerializer,
    CountrySerializer,
    MembershipSerializer,
    PackageSerializer,
)


# Create your views here.


class CountryListCreateAPIView(ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("is_active",)


class CountryRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class CityListCreateAPIView(ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("is_active",)

    def get_queryset(self):
        country = self.kwargs.get("country_id")
        if country:
            return City.objects.filter(country=country)
        return super().get_queryset()


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
        if self.request.user.user_type == UserType.ADMIN:
            return Package.objects.all()
        return Package.objects.filter(is_active=True)


class PackageRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class PackageRetrieveAPIViewByName(RetrieveAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = "name"

    def get_queryset(self):
        return Package.objects.filter(is_active=True)


class MembershipListCreateAPIView(ListCreateAPIView):
    # queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def create(self, request, *args, **kwargs):
        serializer = MembershipSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            id = request.user.id
            user = User.objects.get(id=id)
            if Membership.objects.filter(
                user=user, expire_date__gt=timezone.now()
            ).exists():
                raise serializers.ValidationError(
                    "You have an active membership that expired on, Would like cancel it, and proceed with new membership"
                )

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        # membership_notification()
        user = self.request.user
        if user.user_type == "Admin":
            return Membership.objects.all()
        return Membership.objects.filter(
            user=user, is_pay=True, expire_date__gt=timezone.now()
        )


class ActiveMembershipList(RetrieveAPIView):
    # queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    # lookup_field = 'user.username'

    def get_queryset(self):
        user = self.request.user
        qu = Membership.objects.filter(
            expire_date__gt=timezone.now(), is_pay=True, user=user
        )
        
        return qu

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.first()


class InactiveMembershipList(ListAPIView):
    # queryset = Membership.objects.filter(expire_date__lt=datetime.today())
    serializer_class = MembershipSerializer

    def get_queryset(self):
        user = self.request.user
        return Membership.objects.filter(
            expire_date__lt=timezone.now(), is_pay=True, user=user
        )


class MembershipRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     id = self.kwargs.get('pk')
    #     if user.user_type == UserType.ADMIN:
    #         return super().get_queryset()
    #     return Membership.objects.filter(user=user,is_pay=True,expire_date__lt=timezone.now())

@api_view(["post"])
def get_checkoutid(request, package_id):
    responseData = hyperpay_request()
    return response.Response(
        {
            "data": responseData
        }
    )