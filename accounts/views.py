from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile

try:
    from core.models import StudentProfile
except:
    StudentProfile = None

def register(request):
    if request.user.is_authenticated:
        return redirect("/accounts/dashboard/")

    error_msg = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip() or request.POST.get("gmail", "").strip()
        student_id = request.POST.get("student_id", "").strip()
        password1 = request.POST.get("password1", "").strip() or request.POST.get("password", "").strip()
        password2 = request.POST.get("password2", "").strip() or request.POST.get("confirm_password", "").strip()

        if not username or not email or not password1:
            error_msg = "All fields are required."
        elif password1 != password2:
            error_msg = "Passwords do not match."
        elif len(password1) < 8:
            error_msg = "Password must be at least 8 characters."
        elif User.objects.filter(username=username).exists():
            error_msg = "Username already taken."
        elif User.objects.filter(email=email).exists():
            error_msg = "Email already registered."
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                # Save Student ID to Profile
                try:
                    profile, created = Profile.objects.get_or_create(user=user)
                    profile.student_id = student_id
                    profile.save()
                except Exception:
                    pass
                login(request, user)
                return redirect("/accounts/dashboard/")
            except Exception as e:
                error_msg = f"Error: {str(e)}"

    return render(request, "accounts/register.html", {"error_msg": error_msg, "error": error_msg})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    return render(request, "accounts/dashboard.html")

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
        if request.POST.get("email"):
            request.user.email = request.POST.get("email")
            request.user.save()
        return redirect("profile")
    return render(request, "accounts/profile.html", {"profile": profile})

def make_admin_now(request):
    from django.http import HttpResponse
    username = "negus_admin"
    password = "Negus12345!"
    email = "negus@unima.ac.mw"
    if User.objects.filter(username=username).exists():
        u = User.objects.get(username=username)
        u.set_password(password)
        u.is_staff = True
        u.is_superuser = True
        u.save()
        return HttpResponse(f"Admin UPDATED! {username} / {password}")
    else:
        User.objects.create_superuser(username, email, password)
        return HttpResponse(f"Admin CREATED! {username} / {password}")
