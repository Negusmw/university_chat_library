from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile

try:
    from core.models import StudentProfile
except:
    StudentProfile = None

def register(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1") or request.POST.get("password")
        password2 = request.POST.get("password2") or request.POST.get("confirm_password") or password1

        if not username or not password1:
            error = "Username and password are required."
        elif password1 != password2:
            error = "Passwords do not match."
        elif len(password1) < 8:
            error = "Password must be at least 8 characters."
        elif User.objects.filter(username=username).exists():
            error = "Username already taken, choose another."
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                login(request, user)
                return redirect("/accounts/dashboard/")
            except Exception as e:
                error = f"Error creating account: {str(e)}"

    return render(request, "accounts/register.html", {"error": error, "error_msg": error})
                                 
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
