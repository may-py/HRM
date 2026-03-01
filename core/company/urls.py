from django.urls import path
from .views import (
    CompanyLandingView, 
    CompanyRequestView, 
    RequestSuccessView, 
    AdminDashboardView,
    smart_redirect,
    CompanyRequestDetailView
    )

app_name = 'company'

urlpatterns = [
    path('', CompanyLandingView.as_view(), name='landing'),
    path('apply/', CompanyRequestView.as_view(), name='onboarding'),
    path('success/', RequestSuccessView.as_view(), name='request_success'),
    path('manage/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('home/', smart_redirect, name='smart_redirect'),
    path('manage/request/<int:pk>/', CompanyRequestDetailView.as_view(), name='request_detail'),
]