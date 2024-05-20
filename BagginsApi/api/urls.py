from django.urls import path, include
from .serializers import CookieTokenObtainPairView, CookieTokenRefreshView
from .views import GetPointTurnoverView, GetPointOrderView, GetPointView

urlpatterns = [
    path('', include('djoser.urls')),
    path('get_point_turnover/<int:id>/', GetPointTurnoverView.as_view()),
    path('get_point_order/<int:id>/', GetPointOrderView.as_view()),
    path('get_point_all/<int:id>/', GetPointView.as_view()),
    path('auth/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]
