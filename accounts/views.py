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
        email = request.POST.get('email','').strip()
        student_id = request.POST.get('student_id','').strip()
        password1 = request.POST.get('password1','')
        password2 = request.POST.get('password2','')

        # validation
        if password1 != password2:
            return render(request, 'accounts/register.html', {'error_msg': "Passwords don't match"})
        
        if len(password1) < 8:
            return render(request, 'accounts/register.html', {'error_msg': "Password must be 8+ chars"})

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error_msg': "Username taken"})

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            
            if StudentProfile:
                try:
                    StudentProfile.objects.get_or_create(
                        user=user, 
                        defaults={'student_id': student_id, 'university_email': email}
                    )
                except:
                    pass
            
            login(request, user)
            return redirect('/')
        except Exception as e:
            return render(request, 'accounts/register.html', {'error_msg': f"Error: {e}"})

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
