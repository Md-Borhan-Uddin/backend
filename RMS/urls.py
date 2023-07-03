from RMS import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('api/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('realestate.urls')),
    path('api/', include('settings.urls')),
    path('api/refresh-token/', TokenRefreshView.as_view()),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)




