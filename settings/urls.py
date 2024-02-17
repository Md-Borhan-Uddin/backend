from django.urls import path
from settings.views import (
    ActiveMembershipList,
    AssetRetrieveDestroyAPIView,
    CountryListCreateAPIView,
    CountryRetrieveDestroyAPIView,
    CityListCreateAPIView,
    CityRetrieveDestroyAPIView,
    AssetListCreateAPIView,
    InactiveMembershipList,
    MembershipListCreateAPIView,
    MembershipRetrieveDestroyAPIView,
    PackageListCreateAPIView,
    PackageRetrieveAPIViewByName,
    PackageRetrieveDestroyAPIView,
    get_checkoutid
)






urlpatterns = [
    path('country/', CountryListCreateAPIView.as_view()),
    path('country/<int:pk>/', CountryRetrieveDestroyAPIView.as_view()),
    path('city/', CityListCreateAPIView.as_view()),
    path("city/<int:country_id>/", CityListCreateAPIView.as_view(), name="city_by_country"),
    path('city/edit/<int:pk>/', CityRetrieveDestroyAPIView.as_view()),
    path('city/delete/<int:pk>/', CityRetrieveDestroyAPIView.as_view()),
    path('asset/', AssetListCreateAPIView.as_view()),
    path('asset/<int:pk>/', AssetRetrieveDestroyAPIView.as_view()),
    path('package/', PackageListCreateAPIView.as_view()),
    path('package/<int:pk>/', PackageRetrieveDestroyAPIView.as_view()),
    path('package/<str:name>/', PackageRetrieveAPIViewByName.as_view()),
    path('membership/', MembershipListCreateAPIView.as_view()),
    path('active-membership/', ActiveMembershipList.as_view()),
    path('inactive-membership/', InactiveMembershipList.as_view()),
    path('membership/<int:pk>/', MembershipRetrieveDestroyAPIView.as_view()),
    path('checkout-id/<int:package_id>/', get_checkoutid),
]
