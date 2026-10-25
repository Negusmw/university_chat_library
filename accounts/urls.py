from django.urls import path
from django.contrib.auth import logout, views as auth_views
from django.shortcuts import redirect
from . import views
path('login/', views.custom_login, name='login'),

def logout_get(request):
    logout(request)
    return redirect('/accounts/login/')
    

urlpatterns = [
    # Login
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Register - USES YOUR FIXED views.register, NOT the one inside urls.py
    path('register/', views.register, name='register'),
    
    # Logout
    path('logout/', logout_get, name='logout'),
    
    # Dashboard & Profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Temp - to fix admin
    path('make-admin/', views.make_admin_now, name='make_admin'),
]
