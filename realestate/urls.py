from django.urls import path

from .views import (
    AssertBrandListCreateAPIView,
    AssertBrandRetrieveDestroyAPIView,
    AssertTypeListCreateAPIView,
    AssertTypeRetrieveDestroyAPIView,
    AssetByRealestate,
    AssetListAPIView,
    AssetRetrieveUpdateDestroyAPIView,
    RealEstateAPI,
    RealestateCount,
    RealEstateDetailAPIView,
    RealEstateRetrieveDestroyAPIView,
    RealestateSearchAPIView,
    RealEstateTypeListCreateAPIView,
    RealEstateTypeRetrieveDestroyAPIView,
    RealestateUpdateAPIView,
    ScheduleMaintainesListAPIView,
    ScheduleMaintainesRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("real-estate-type/", RealEstateTypeListCreateAPIView.as_view()),
    path("real-estate-type/<int:pk>/", RealEstateTypeRetrieveDestroyAPIView.as_view()),
    path("assets/", AssetListAPIView.as_view(), name="assets"),
    path(
        "assets/<int:pk>/",
        AssetRetrieveUpdateDestroyAPIView.as_view(),
        name="asserts_rud",
    ),
    path("asset-by/<int:pk>/", AssetByRealestate.as_view(), name="asset_by"),
    path("assert-type/", AssertTypeListCreateAPIView.as_view()),
    path("assert-type/<int:pk>/", AssertTypeRetrieveDestroyAPIView.as_view()),
    path("assert-brand/", AssertBrandListCreateAPIView.as_view()),
    path("assert-brand/<int:pk>/", AssertBrandRetrieveDestroyAPIView.as_view()),
    path("realestate/<str:usertype>/", RealEstateAPI.as_view(), name="realestate_list"),
    path(
        "realestate/edit/<int:pk>/",
        RealestateUpdateAPIView.as_view(),
        name="realestate_edit",
    ),
    path(
        "realestate/delete/<int:pk>/",
        RealEstateRetrieveDestroyAPIView.as_view(),
        name="realestate_delete",
    ),
    path("realestate-count/", RealestateCount.as_view(), name="realestate_count"),
    path(
        "realestate/<int:pk>/detail/",
        RealEstateRetrieveDestroyAPIView.as_view(),
        name="realestate_by_id",
    ),
    path(
        "real-estate/details/",
        RealEstateDetailAPIView.as_view(),
        name="realestate_details",
    ),
    path(
        "schedule-maintain/",
        ScheduleMaintainesListAPIView.as_view(),
        name="schedule_maintaines",
    ),
    path(
        "schedule-maintain/<int:pk>/",
        ScheduleMaintainesRetrieveUpdateDestroyAPIView.as_view(),
        name="schedule_maintaines",
    ),
    path(
        "search-realestate/",
        RealestateSearchAPIView.as_view(),
        name="realestate_search",
    ),
]
