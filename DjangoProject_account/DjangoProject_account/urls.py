"""
URL configuration for DjangoProject_account project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from accounting import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet, basename='user')
# router.register(r'categories', views.CategoryViewSet, basename='category')
# router.register(r'transactions', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('accounting.urls')),
]
