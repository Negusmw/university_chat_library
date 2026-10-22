from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views
from django.contrib.auth import logout, views as auth_views
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login
from core.views import register_view, profile_view

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
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/', profile_view, name='profile'),
    path('', core_views.home, name='home'),
    # ... your other paths
    path('dashboard/', core_views.dashboard, name='dashboard'),  # for Home button
    path('accounts/dashboard/', core_views.dashboard, name='student_dashboard'),  # for old link
    path('profile/', core_views.profile, name='profile'),
    path('accounts/profile/', core_views.profile, name='accounts_profile'),
    path('accounts/logout/', core_views.logout_view, name='logout'),
    path('logout/', core_views.logout_view, name='logout2'),
    path('my-admin/', core_views.admin_hub, name='my_admin'),
    path('library/', core_views.library, name='library'),
    path('chat/', core_views.chat, name='chat'),
    path('community/', include('community.urls')),  # <-- THIS LINE MUST BE HERE
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/register/', register_view, name='register'),
    path('accounts/logout/', logout_get, name='logout'),
]

# THIS IS THE FIX FOR VIDEOS
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)