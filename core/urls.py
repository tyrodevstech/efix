from unicodedata import name
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views #import this
from . import views

urlpatterns = [
    path('', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('registration/', views.registration_view, name = 'registration'),

    path('dashboard/', views.dashboard_view, name = 'dashboard'),
    path('dashboard/update/<str:pk>', views.updateProfile_view, name = 'updateProfile'),
    path('dashboard/change_password/', views.changePassword_view, name='changePassword'),
    path('dashboard/request_service/', views.create_service_view, name = 'create_service'),
    path('dashboard/service_request_list/', views.service_request_list_view, name = 'service_request_list'),
    path('dashboard/work_request_list/', views.work_request_list_view, name = 'work_request_list'),
    path('dashboard/details/service/<str:pk>', views.details_service_view, name = 'details_service'),
    path('send_invoice', views.admin_invoice_view, name = 'send_invoice'),
    path('get_service_data', views.admin_servicelist_view, name = 'get_service_data'),

    path('api/satus_update', views.satusUpdate, name = 'satusUpdate'),
    path('api/district', views.getDistrict_view, name = 'getDistrict'),
    path('api/upazila', views.getUpazila_view, name = 'getUpazila'),
    path('api/getEmail', views.getEmail_view, name = 'getEmail'),
    path('api/getPhone', views.getPhone_view, name = 'getPhone'),

    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),

    path('get_technician_work_list/',views.get_technician_work_list,name='technician_work_list')
]