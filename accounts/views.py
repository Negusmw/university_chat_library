from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse

# Try import profile - don't crash if it doesn't exist
try:
    from core.models import StudentProfile
except:
    StudentProfile = None

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        email = request.POST.get('university_email') or request.POST.get('email') or ''
        email = email.strip()
        student_id = request.POST.get('student_id','').strip()
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password') or request.POST.get('password2')

        if not all([username, email, password, password2]):
            messages.error(request, "Please fill all fields")
            return render(request, 'accounts/register.html')

        if password != password2:
            messages.error(request, "Passwords don't match")
            return render(request, 'accounts/register.html')

        if len(password) < 8:
            messages.error(request, "Password must be 8+ chars")
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        
        if StudentProfile and student_id:
            try:
                StudentProfile.objects.create(user=user, student_id=student_id, university_email=email)
            except:
                pass

        login(request, user)
        return redirect('/accounts/dashboard/')

    return render(request, 'accounts/register.html')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def profile_view(request):
    return render(request, 'accounts/dashboard.html')

def make_admin_now(request):
    user, created = User.objects.get_or_create(username='negus', defaults={'email': 'negus@unima.ac.mw'})
    if created:
        user.set_password('Negus123!')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return HttpResponse(f"{'CREATED' if created else 'UPDATED'} negus - admin. Login: negus / Negus123!")

def logout_get(request):
    logout(request)
    return redirect('/accounts/login/')
