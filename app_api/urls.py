from django.db import router
from django.urls import path
from app_api.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'admin',AdminViewSet)
# router.register(r'car',CarViewSet,basename='car')
# router.register(r'rentcar',RentCarViewSet,basename='rentcars')

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls