from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile

try:
    from core.models import StudentProfile
except:
    StudentProfile = None

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "").strip()
        
        # Force unique username/email to avoid "already taken"
        import time
        if User.objects.filter(username=username).exists():
            username = f"{username}{int(time.time())%1000}"
        if User.objects.filter(email__iexact=email).exists():
            email = f"{int(time.time())}@test.com"

        user = User.objects.create_user(username=username, email=email, password=password1)
        Profile.objects.get_or_create(user=user)
        if StudentProfile:
            try:
                StudentProfile.objects.get_or_create(user=user, defaults={'student_id': f"STU{user.id:06d}"})
            except:
                pass
        login(request, user)
        return redirect("/")

    return render(request, "accounts/register.html")

    return render(request, "accounts/register.html", {"error_msg": error})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    return render(request, "accounts/dashboard.html")

from django.contrib.auth.decorators import login_required
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.full_name = request.POST.get("full_name")
        profile.student_id = request.POST.get("student_id")
        profile.course = request.POST.get("course")
        profile.year_of_study = request.POST.get("year_of_study")
        profile.bio = request.POST.get("bio")
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        request.user.email = request.POST.get("email")
        request.user.save()
        return redirect("profile")
    return render(request, "accounts/profile.html", {"profile": profile})
