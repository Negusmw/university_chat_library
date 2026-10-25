from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

try:
    from core.models import StudentProfile
except:
    StudentProfile = None

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        email = request.POST.get('email') or request.POST.get('university_email') or ''
        email = email.strip()
        student_id = request.POST.get('student_id','')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password') or request.POST.get('password2') or password

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username taken")
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        if StudentProfile:
            try:
                StudentProfile.objects.create(user=user, student_id=student_id, university_email=email)
            except: pass

        login(request, user)
        return redirect('/')  # or '/accounts/dashboard/' - goes to home after register

    return render(request, 'accounts/register.html')

def custom_login(request):
    # THIS matches your real screenshot: Username + Password only
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')  # FIX: now it will redirect, not stay same
        else:
            messages.error(request, "Wrong username or password")
    
    return render(request, 'accounts/login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    return render(request, 'accounts/dashboard.html')

def logout_get(request):
    logout(request)
    return redirect('/accounts/login/')

def make_admin_now(request):
    user, _ = User.objects.get_or_create(username='negus', defaults={'email':'negus@unima.ac.mw'})
    user.set_password('Negus123!')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return HttpResponse("Admin ready: negus / Negus123!")
