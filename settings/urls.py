from django.urls import path
from settings.views import *






urlpatterns = [
    path('country/', CountryListCreateAPIView.as_view()),
    path('country/<int:pk>/', CountryRetrieveDestroyAPIView.as_view()),
    path('city/', CityListCreateAPIView.as_view()),
    path('city/<int:pk>/', CityRetrieveDestroyAPIView.as_view()),
    path('asset/', AssetListCreateAPIView.as_view()),
    path('asset/<int:pk>/', AssetRetrieveDestroyAPIView.as_view()),
    path('package/', PackageListCreateAPIView.as_view()),
    path('package/<int:pk>/', PackageRetrieveDestroyAPIView.as_view()),
    path('package/<str:name>/', PackageRetrieveAPIViewByName.as_view()),
    path('membership/', MembershipListCreateAPIView.as_view()),
    path('active-membership/', ActiveMembershipList.as_view()),
    path('inactive-membership/', InactiveMembershipList.as_view()),
    path('membership/<int:pk>/', MembershipRetrieveDestroyAPIView.as_view()),
]
