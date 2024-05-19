from django.contrib import admin
from django.urls import path, include

from .serializers import CookieTokenObtainPairView, CookieTokenRefreshView

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]
