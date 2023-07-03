from django.urls import path
from accounts.views import (
    AdminListApiView, RealTorApiView, 
    UserApiView, EmailVeryfi, LoginAPIView, 
    UpdateUserAPIView,UserRetrieveDestroyAPIView,
    ResendEmail
    )


urlpatterns = [
    path('admin/registration/', AdminListApiView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('realtor/registration/', RealTorApiView.as_view()),
    path('user-edit/<int:pk>/', UpdateUserAPIView.as_view()),
    path('user/', UserRetrieveDestroyAPIView.as_view()),
    path('all-user/', UserApiView.as_view()),
    path('email-veryfi/<uid>/<token>/', EmailVeryfi.as_view(), name="veryfi_email"),
    path('resend-activation/', ResendEmail.as_view(), name="resend_activation"),
]
