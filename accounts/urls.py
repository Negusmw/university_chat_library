from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views

def logout_get(request):
    logout(request)
    return redirect('/accounts/login/')

urlpatterns = [
    # Login - uses your custom design
    path('login/', views.custom_login, name='login'),
    
    # Register
    path('register/', views.register, name='register'),
    
    # Logout
    path('logout/', logout_get, name='logout'),
]
