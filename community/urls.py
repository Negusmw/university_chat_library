from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_list, name='community_list'),
    path('', views.community_list, name='community'),  # alias for your template
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('<int:group_id>/join/', views.join_group, name='join_group'),
    path('<int:group_id>/leave/', views.leave_group, name='leave_group'),
    path('<int:group_id>/chat/', views.group_chat, name='group_chat'),
    path('<int:group_id>/messages/json/', views.chat_messages_json, name='chat_messages_json'),
]