from .views import (
    RealEstateTypeListCreateAPIView, RealEstateAPI, 
    RealestateUpdateAPIView, RealestateDeleteAPIView,
    RealEstateTypeRetrieveDestroyAPIView, AssertTypeRetrieveDestroyAPIView, 
    AssertTypeListCreateAPIView, AssertBrandListCreateAPIView, AssertBrandRetrieveDestroyAPIView,
    ScheduleMaintainesListAPIView, ScheduleMaintainesRetrieveUpdateDestroyAPIView, AssetListAPIView,
    AssetByRealestate, RealestateCount
    )
from django.urls import path

urlpatterns = [
    path('real-estate-type/',RealEstateTypeListCreateAPIView.as_view()),
    path('real-estate-type/<int:pk>/',RealEstateTypeRetrieveDestroyAPIView.as_view()),

    path('asset/', AssetListAPIView.as_view(), name='asset'),
    path('asset-by/<int:pk>/', AssetByRealestate.as_view(), name='asset_by'),

    path('assert-type/',AssertTypeListCreateAPIView.as_view()),
    path('assert-type/<int:pk>/',AssertTypeRetrieveDestroyAPIView.as_view()),

    path('assert-brand/',AssertBrandListCreateAPIView.as_view()),
    path('assert-brand/<int:pk>/',AssertBrandRetrieveDestroyAPIView.as_view()),


    path('realestate/<str:usertype>/', RealEstateAPI.as_view(), name='realestate_list'),
    path('realestate/edit/<int:pk>/', RealestateUpdateAPIView.as_view(), name='realestate_edit'),
    path('realestate/delete/<int:pk>/', RealestateDeleteAPIView.as_view(), name='realestate_delete'),
    path("realestate-count/", RealestateCount.as_view(), name="realestate_count"),
    
    path('schedule-maintain/',ScheduleMaintainesListAPIView.as_view(), name='schedule_maintaines'),
    path('schedule-maintain/<int:pk>/',ScheduleMaintainesRetrieveUpdateDestroyAPIView.as_view(), name='schedule_maintaines'),
]