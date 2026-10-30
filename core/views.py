from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from .models import PROGRAM_CHOICES
from .models import ChatMessage, Resource
from .models import StudentProfile
import os

def home(request):
    return render(request, "core/home.html")

@login_required(login_url="/accounts/login/")
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/accounts/login/')
def profile(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        sid = request.POST.get('student_id','').strip().upper()
        if sid and profile.student_id in ["", "NOT SET", None]:
            if not StudentProfile.objects.filter(student_id=sid).exists():
               profile.student_id = sid
               profile.save()
               return redirect('profile')

    return render(request, 'profile.html', {
        'profile': profile
})

@login_required
def profile_view(request):
    from .models import StudentProfile
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        if student_id:
            profile.student_id = student_id
            profile.save()
            messages.success(request, f"Student ID {student_id} saved!")
            return redirect('/profile/')
    
    return render(request, 'core/profile.html', {
        'profile': profile,
        'user_obj': request.user,
    })

@login_required(login_url="/accounts/login/")
def library(request):
    resources = Resource.objects.all().order_by('-created_at')
    query = request.GET.get('q','')
    program = request.GET.get('program','')
    year = request.GET.get('year','')
    course = request.GET.get('course','')

    if query:
        resources = resources.filter(title__icontains=query)
    if program:
        resources = resources.filter(program=program)
    if year:
        resources = resources.filter(year=year)
    if course:
        resources = resources.filter(course_code__icontains=course)

    return render(request, 'core/library.html', {
        'resources': resources,
        'program_choices': PROGRAM_CHOICES,
    })

@login_required(login_url="/accounts/login/")
def chat(request):
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        message_type = request.POST.get("message_type", "text")
        uploaded_file = request.FILES.get("file")

        if uploaded_file:
            name = uploaded_file.name.lower()
            _, ext = os.path.splitext(name)
            if ext in ['.mp3', '.m4a', '.wav', '.ogg', '.webm'] and message_type != 'video':
                if 'voice' in name or message_type == 'voice':
                    message_type = 'voice'
                elif ext == '.webm' and uploaded_file.size > 500000:
                    message_type = 'video'
                else:
                    if ext != '.webm':
                        message_type = 'voice'
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                message_type = 'photo'
            elif ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
                if message_type != 'voice':
                    message_type = 'video'

        if message or uploaded_file:
            ChatMessage.objects.create(
                user=request.user,
                message=message,
                message_type=message_type,
                file=uploaded_file if uploaded_file else None
            )
        return redirect("chat")

    chat_messages = ChatMessage.objects.select_related("user").order_by("created_at")
    online_users = User.objects.filter(is_active=True).order_by('-last_login')[:15]

    return render(request, "core/chat.html", {
        "chat_messages": chat_messages,
        "online_users": online_users
    })

@login_required(login_url="/accounts/login/")
def community(request):
    from community.models import StudyGroup
    groups = StudyGroup.objects.all()
    return render(request, 'community/community.html', {'groups': groups})

@staff_member_required
def admin_hub(request):
    total_users = User.objects.count()
    staff_users = User.objects.filter(is_staff=True).count()
    return render(request, 'admin_hub.html', {
        'total_users': total_users,
        'staff_users': staff_users,
        'users': User.objects.all().order_by('-date_joined')[:10]
    })

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')
