from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='core_dashboard'),
    path('profile/', views.profile, name='core_profile'),
    path('library/', views.library, name='library'),
    path('chat/', views.chat, name='chat'),
    path('community/', views.community, name='community'),
    path('admin-hub/', views.admin_hub, name='admin_hub'),
    path('logout-view/', views.logout_view, name='core_logout'),
]
