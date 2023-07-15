from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import UserType
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from utils.pagination import PaginationWithPageNumber
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from settings.models import Membership
from settings.tasks import notification
# Create your views here.

class RealEstateTypeListCreateAPIView(ListCreateAPIView):
    queryset = RealEstateType.objects.all()
    serializer_class = RealEstateTypeSerializers



class RealEstateTypeRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = RealEstateType.objects.all()
    serializer_class = RealEstateTypeSerializers

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)





class AssertTypeListCreateAPIView(ListCreateAPIView):
    queryset = AssertType.objects.all()
    serializer_class = AssertTypeSerializers



class AssertTypeRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AssertType.objects.all()
    serializer_class = AssertTypeSerializers



class AssertBrandListCreateAPIView(ListCreateAPIView):
    queryset = AssertBrand.objects.all()
    serializer_class = AssertBrandSerializers



class AssertBrandRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AssertBrand.objects.all()
    serializer_class = AssertBrandSerializers


class RealestateUpdateAPIView(APIView):
    def get(self,request,pk,*args, **kwargs):
        # if RealEstate.objects.get(id=pk).exist():
        #     return Response({"message":"Realestate Not Found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            obj = RealEstate.objects.get(id=pk)
            serializer = RealEstateUpdateSerializer(obj, context={"request":request})
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
             return Response({"message":"Realestate Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self,request,pk,*args, **kwargs):
        print(request.data)
        serializer = RealEstateSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            re = serializer.save(location='dhaka')
            
            data = {
                'message':"RealEstate Save Successfully",
                
            }
            return Response(data,status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RealestateDeleteAPIView(APIView):
    def delete(self, request,pk, *args, **kwargs):
        re = RealEstate.objects.get(id=pk)
        re.delete()
        return Response({"message":"delete successfully"})


class RealestateCount(APIView):
    def get(self, request, *args, **kwargs):
        country = RealEstate.objects.values('country').annotate(totalnumber=Count('country'))
        city = RealEstate.objects.values('city').annotate(totalnumber=Count('city')) 
        type = RealEstate.objects.values('type').annotate(totalnumber=Count('type'))
        data = {
            'country':country,
            'city':city,
            'type':type
        }
        return Response(data=data)

class RealEstateRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = RealEstate.objects.all()
    serializer_class = RealEstateSerializer

    # def get_queryset(self):
    #     print(self.request)
    #     return super().get_queryset()


class RealEstateAPI(APIView):
    def get(self, request,usertype, *args, **kwargs):
        
        obj = RealEstate.objects.all()
        
        if usertype != UserType.ADMIN:
        
            obj = RealEstate.objects.filter(user = request.user.id)
            
        
        serializer = RealEstateSerializer(obj, many = True, context = {"request":request})
        return Response(data=serializer.data)
    

    def post(self, request, *args, **kwargs):
        if Membership.object.filter(user=request.user.id,expire_date__gt=datetime.now(),is_pay=True).exists():
            serializer = RealEstateSerializer(data=request.data, context = {"request":request})
            if serializer.is_valid():
                re = serializer.save()
                
                data = {
                    'message':"RealEstate Save Successfully",
                    
                }
                return Response(data,status=status.HTTP_201_CREATED)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'message':'You dont have active membership'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
class AssetByRealestate(APIView):

    def get(self, request, pk, *args, **kwargs):
        real_estate = RealEstate.objects.get(id=pk)
        asset = Assert.objects.filter(real_estate=real_estate)
        serializer = AssertSerializer(asset,many=True, context = {"request":request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class AssetListAPIView(ListCreateAPIView):
    queryset = Assert.objects.all()
    serializer_class = AssertSerializer


    

class ScheduleMaintainesListAPIView(ListCreateAPIView):
    # queryset = ScheduleMaintaines.objects.all()
    serializer_class = ScheduleMaintainesSerializer
    pagination_class = PaginationWithPageNumber
    

    def get_queryset(self):
        notification()
        obj = None
        user = self.request.user
        obj = ScheduleMaintaines.objects.all()
        if user.user_type!='Admin':
            obj = ScheduleMaintaines.objects.filter(real_estate__user=user)
        
        return obj


class ScheduleMaintainesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ScheduleMaintaines.objects.all()
    serializer_class = ScheduleMaintainesSerializer


