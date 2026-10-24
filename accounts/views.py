from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def register(request):
    error_msg = None
    
    if request.user.is_authenticated:
        return redirect("/accounts/dashboard/")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()

        if not username or not email or not password1:
            error_msg = "All fields are required."
        elif password1 != password2:
            error_msg = "Passwords do not match."
        elif len(password1) < 8:
            error_msg = "Password must be at least 8 characters."
        elif User.objects.filter(username=username).exists():
            error_msg = f"Username '{username}' already taken."
        else:
            try:
                # Create user ONLY - no Profile to avoid crash
                user = User.objects.create_user(username=username, email=email, password=password1)
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
    from .models import Profile
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
        return redirect("profile")
    return render(request, "accounts/profile.html", {"profile": profile})

def make_admin_now(request):
    username = "negus_admin"
    password = "Negus12345!"
    email = "negus@unima.ac.mw"
    if User.objects.filter(username=username).exists():
        u = User.objects.get(username=username)
        u.set_password(password)
        u.is_staff = True
        u.is_superuser = True
        u.save()
        return HttpResponse(f"UPDATED {username} / {password}")
    else:
        User.objects.create_superuser(username, email, password)
        return HttpResponse(f"CREATED {username} / {password}")
