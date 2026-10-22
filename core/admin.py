from django.contrib import admin
from .models import ChatMessage, Resource, StudentProfile

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'course_code', 'year', 'created_at')
    list_filter = ('program', 'year')
    search_fields = ('title', 'course_code')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'gmail')

    search_fields = ('user__username', 'student_id')