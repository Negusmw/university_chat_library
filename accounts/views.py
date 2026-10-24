from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse

def register(request):
    error_msg = None
    if request.user.is_authenticated:
        return redirect("/accounts/dashboard/")
    if request.method == "POST":
        username = request.POST.get("username","").strip()
        email = request.POST.get("email","").strip()
        p1 = request.POST.get("password1","").strip()
        p2 = request.POST.get("password2","").strip()
        if not username or not email or not p1:
            error_msg = "All fields required."
        elif p1 != p2:
            error_msg = "Passwords do not match."
        elif len(p1) < 8:
            error_msg = "Password too short."
        elif User.objects.filter(username=username).exists():
            error_msg = "Username taken."
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=p1)
                login(request, user)
                return redirect("/accounts/dashboard/")
            except Exception as e:
                error_msg = f"Error: {e}"
    return render(request, "accounts/register.html", {"error_msg": error_msg, "error": error_msg})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    return render(request, "accounts/dashboard.html")

def profile_view(request):
    from .models import Profile
    from django.contrib.auth.decorators import login_required
    profile, _ = Profile.objects.get_or_create(user=request.user)
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
    u,p,e = "negus_admin","Negus12345!","negus@unima.ac.mw"
    if User.objects.filter(username=u).exists():
        x=User.objects.get(username=u)
        x.set_password(p); x.is_staff=True; x.is_superuser=True; x.save()
        return HttpResponse(f"UPDATED {u} / {p}")
    else:
        User.objects.create_superuser(u,e,p)
        return HttpResponse(f"CREATED {u} / {p}")
