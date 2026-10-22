from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Your passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken.")
            return redirect("register")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "That email is already registered.")
            return redirect("register")

        if len(password1) < 8:
            messages.error(request, "Your password must have at least 8 characters.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )
        login(request, user)
        return redirect("dashboard")

    return render(request, "accounts/register.html")

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
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
        request.user.email = request.POST.get("email")
        request.user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "accounts/profile.html", {"profile": profile})