from django.urls import path
from accounting import views
from .views import StatisticsAPIView,indexStatisticsAPIView
urlpatterns = [
    #FBV
    path('users/profile/', views.user_profile, name='user-profile'),
    path('users/register/', views.user_register, name='user_register'),
    path('users/login/', views.user_login, name='user_login'),
    path('transaction/create/', views.transaction_create, name='transaction_create'),
    path('transaction/get/', views.transaction_get, name='transaction_list'),
    path('stats/', StatisticsAPIView.as_view(), name='stats'),
    path('stats/index/', indexStatisticsAPIView.as_view(), name='stats_index'),
]