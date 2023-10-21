from django.urls import path
from accounts.views import (
    AdminListApiView, RealTorApiView, RequestAPIView, RequestSearchAPIView,
    UserApiView, AcctiveAccount, LoginAPIView, NotificationListView,
    UpdateUserAPIView,UserRetrieveDestroyAPIView,
    ResendEmail, UserChangepassword, SendPasswordResetEmail, ResetPassword,
    UserRetrieveAPIView
    )


urlpatterns = [
    path('admin/registration/', AdminListApiView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('realtor/registration/', RealTorApiView.as_view()),
    path("update-user/<str:username>/", RealTorApiView.as_view(), name="user_update"),
    path('user-edit/<str:username>/', UpdateUserAPIView.as_view()),
    path("user-delete/<int:pk>/", UserRetrieveDestroyAPIView.as_view(), name="user_delete"),
    path('user/<int:pk>/', UserRetrieveDestroyAPIView.as_view()),
    path('user/', UserRetrieveAPIView.as_view()),
    path('all-user/', UserApiView.as_view()),
    path("password-change/", UserChangepassword.as_view(), name="password_change"),
    path('active-account/<uid>/<token>/', AcctiveAccount.as_view(), name="veryfi_email"),
    path('resend-activation/', ResendEmail.as_view(), name="resend_activation"),
    path("password-reset-email/", SendPasswordResetEmail.as_view(), name="send_password_email"),
    path("reset-password/<uid>/<token>/", ResetPassword.as_view(), name="reset_password"),

    path("notification/", NotificationListView.as_view(), name="notification"),

    path("visitor-request/", RequestAPIView.as_view(), name="visitor_request"),
    path("request-search/", RequestSearchAPIView.as_view(), name="request_search"),
]
