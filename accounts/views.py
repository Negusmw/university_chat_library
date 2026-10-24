from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse

def register(request):
    if request.user.is_authenticated:
        return redirect("/accounts/dashboard/")
    if request.method == "POST":
        username = request.POST.get("username","").strip()
        email = request.POST.get("email","").strip()
        p1 = request.POST.get("password1","").strip()
        p2 = request.POST.get("password2","").strip()
        
        # DEBUG - show us what happens
        if User.objects.filter(username=username).exists():
            return HttpResponse(f"DEBUG: Username {username} already exists - try new name")
        
        try:
            user = User.objects.create_user(username=username, email=email, password=p1)
            login(request, user)
            return HttpResponse(f"DEBUG SUCCESS: User {username} created and logged in! Now we know register works. Go to /accounts/dashboard/")
        except Exception as e:
            return HttpResponse(f"DEBUG ERROR: {str(e)} | Type: {type(e).__name__}")
    
    return render(request, "accounts/register.html", {"error_msg": None})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    return render(request, "accounts/dashboard.html")

def profile_view(request):
    return render(request, "accounts/dashboard.html")

def make_admin_now(request):
    u,p,e = "negus_admin","Negus12345!","negus@unima.ac.mw"
    if User.objects.filter(username=u).exists():
        x=User.objects.get(username=u)
        x.set_password(p); x.is_staff=True; x.is_superuser=True; x.save()
        return HttpResponse(f"UPDATED {u} / {p}")
    else:
        User.objects.create_superuser(u,e,p)
        return HttpResponse(f"CREATED {u} / {p}")
