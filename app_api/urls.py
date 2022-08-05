from django.db import router
from django.urls import path
from app_api.token import EmailTokenObtainPairView
from app_api.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'admin',AdminViewSet)
router.register(r'account',CustomUserRegistraionViewSet,basename='customuserregistration')
router.register(r'service_request',ServiceRequestViewSet,basename='service_request')
router.register(r'invoice',InvoiceViewSet,basename='invoice')
router.register(r'area',AreaViewSet,basename='area')
router.register(r'division',DivisionViewSet,basename='division')
router.register(r'district',DistrictViewSet,basename='district')
router.register(r'upazila',UpazilaViewSet,basename='upazila')
router.register(r'userdevicetoken',NotificationTokenViewSet,basename='userdevicetoken')

urlpatterns = [
    path('token', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('download-invoice/<int:pk>', render_pdf_view, name='invoice'),
    path('transaction', TransactionView.as_view(), name='transaction'),
] + router.urls