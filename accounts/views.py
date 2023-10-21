#django rest framework import
from rest_framework.response import Response
from accounts.serializers import *
from rest_framework.generics import (
    ListAPIView,ListCreateAPIView, 
    RetrieveDestroyAPIView, UpdateAPIView, 
    DestroyAPIView, RetrieveAPIView
    )
from rest_framework.views import APIView
from rest_framework.validators import ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework.backends import DjangoFilterBackend

#django import 
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate

#project import 
from accounts.models import Admin,RealTor, User, UserType, Notification
from utils.pagination import PaginationWithPageNumber
from accounts.email import ActivationEmail, PasswordResetEmail
from realestate.models import RealEstate
from RMS.celery import debug_task

# Create your views here.



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class AdminListApiView(APIView,):
    
    def get(self,request, *args, **kwargs):
        qs = Admin.objects.all()
        user = UserCreateSerializer(qs, many=True)
        return Response(user.data)
    

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(user_type=UserType.ADMIN)
            return Response(user.data)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class RealTorApiView(ListCreateAPIView):
    queryset = RealTor.objects.all()
    serializer_class = UserCreateSerializer
    pagination_class = PaginationWithPageNumber

    def get(self, request, id=None, *args, **kwargs):
        if id==None:
            user = RealTor.objects.all()
            serializer = UserSerializer(user,many=True)
            return Response({'user':serializer.data}, status=status.HTTP_200_OK)
        user = RealTor.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response({'user':serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(user_type=UserType.REALTOR,is_active=False)
            context = {'user':user}
            ActivationEmail(request, context).send([user.email])
            
            return Response({"messages":"To active Account Veryfi Your Email. Send Email To active Account"}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        # print(self.kwargs)
        obj = User.objects.get(username=username)
        serializer = UserCreateSerializer(obj,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'mesage':'User Update Successfully'}, status=status.HTTP_200_OK)



class ResendEmail(APIView):
    query = RealTor.objects.all()
    serializer_class = EmailSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')

            user = RealTor.objects.filter(email=email)
            if not user.exists():
                return Response({"messages":"This Email Not Registred"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if user[0].is_active:
                return Response({"messages":"You Are already Active User"}, status=status.HTTP_409_CONFLICT)
            context = {'user':user[0]}
            ActivationEmail(request, context).send([user[0].email])
            
            return Response({"messages":"To active Account Veryfi Your Email. Send Email To active Account"}, status=status.HTTP_200_OK)
        else:
            
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)




class AcctiveAccount(APIView):
    def post(self,request,uid,token, *args, **kwargs):
        id = smart_str(urlsafe_base64_decode(uid))
        try:
            user = User.objects.get(id=id)
        except:
            return Response({"message":"User dose not Exist"}, status=status.HTTP_404_NOT_FOUND)
        user_token = get_tokens_for_user(user)
        try:
            if not default_token_generator.check_token(user,token):
                raise ValidationError("Token Is invalid or Expired")
            if user is not None:
                user.is_active = True
                user.save()
                return Response({"message":"Account Activate",'user_type':user.user_type,'token':user_token})
        except DjangoUnicodeDecodeError as identifire:
            default_token_generator.check_token(user,token)
            raise ValidationError("Token Is invalid or Expired")


class SendPasswordResetEmail(APIView):
    def post(self,request, *args, **kwargs):
        print('data',request.data)
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        
        user = User.objects.filter(email=email)
        if not user.exists():
            return Response({"messages":"This Email Not Registred"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        context = {'user':user.first()}
        PasswordResetEmail(request, context).send([user.first().email])

        return Response({'message':'Email Send Successfully'})

class ResetPassword(APIView):
    def post(self,request,uid,token, *args, **kwargs):
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        
        user_token = get_tokens_for_user(user)
        serializers = UserChangePasswordSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        password = serializers.data.get('new_password')
        try:
            if not default_token_generator.check_token(user,token):
                raise ValidationError("Token Is invalid or Expired")
            if user is not None:
                user.set_password(password)
                user.save()
                return Response({"message":"Password change Successfully"})
        except DjangoUnicodeDecodeError as identifire:
            default_token_generator.check_token(user,token)
            raise ValidationError("Token Is invalid or Expired")
        




class UserApiView(ListAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PaginationWithPageNumber

    def get_queryset(self):
        
        debug_task.delay(self.request.user.username)
        return User.objects.defer('date_joined')
    
    

class UpdateUserAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    lookup_field = 'username'
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     print(self.request.data)
    #     return super().get_queryset()

# class UserDestroyAPIView(DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        request = self.request
        user = request.user
        return user

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    token = get_tokens_for_user(user)
                    res = {
                        'message':'Login Successfull',
                        'user':UserSerializer(user).data,
                        'token':token
                    }
                    return Response(res,status=status.HTTP_200_OK)
                else:
                    return Response({"message":"Account Is Not Activate"},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message":"Sorry wrong user name or password"},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors)



class UserChangepassword(APIView):
    def post(self, request, *args, **kwargs):
        
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_password = serializer.data.get('new_password')
        
        if new_password:
            user = request.user
            if user.check_password(new_password):
                return Response({'message':'You have given new password same as the old one. Give new password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'message':'Password change Succesfully'})
        return Response({'message':'Somethings Wrong'})


    

class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(to=user.id)



class RequestAPIView(ListCreateAPIView):
    serializer_class = RequestSerializer

    def create(self, request, *args, **kwargs):
        obj = super().create(request, *args, **kwargs)
        data = obj.data
        print(obj.data)
        real_estate = RealEstate.objects.get(id=data.get('real_estate'))
        Notification.objects.create(
            subject = 'Visitor Request',
            body = f"Dear {real_estate.user.username} new request – {data.get('id')} has been received and waiting your approval to share your real estate {real_estate.name} information with the {data.get('first_name')}",
            to=real_estate.user
        )
        return obj

    def get_queryset(self):
        user = self.request.user
        
        return Visitor.objects.filter(realestate__user=user)



class RequestSearchAPIView(ListAPIView):
    queryset = Visitor.objects.all()
    serializer_class = RequestSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = serializer_class.Meta.fields#('id','first_name','last_name','create','update','real_estate__user')


    # def get_queryset(self):
    #     user = self.request.user
        
    #     print(self.request.query_params)
    #     print(self.serializer_class.Meta.fields)
        
    #     return Visitor.objects.all()
    