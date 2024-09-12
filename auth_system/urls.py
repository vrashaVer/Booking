from django.urls import path
from auth_system import views

urlpatterns = [
    path("register/",views.register,name='register'),
    path("login/",views.login_view,name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('account_activation_invalid/', views.account_activation_invalid, name='account_activation_invalid'),
]