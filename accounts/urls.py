from django.urls import path
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

def logout_get(request):
    logout(request)
    return redirect('/')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('/')
    return render(request, 'registration/register.html')

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_get, name='logout'),
]