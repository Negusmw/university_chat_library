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
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()

        print(f"Trying to register: {username} {email}")  # This will show in Vercel Logs

        if not username or not email or not password1:
            error = "Please fill all fields."
        elif password1 != password2:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = f"Username '{username}' is already taken."
        elif User.objects.filter(email__iexact=email).exists():
            error = "That email is already registered."
        elif len(password1) < 8:
            error = "Password must be at least 8 characters."
        else:
            # ALL GOOD - CREATE USER
            user = User.objects.create_user(username=username, email=email, password=password1)
            Profile.objects.get_or_create(user=user)
            if StudentProfile:
                StudentProfile.objects.get_or_create(user=user, defaults={'student_id': f"STU{user.id:06d}"})
            login(request, user)
            print(f"User {username} created successfully!")
            return redirect("/")  # Go to home, not dashboard to avoid URL error

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
