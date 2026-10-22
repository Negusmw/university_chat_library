from django.contrib import admin
from .models import StudyGroup, GroupMessage

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'created_at')
    filter_horizontal = ('members',)

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'sender', 'content', 'created_at')