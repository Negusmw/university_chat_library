from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile
from .validators import validate_unima_student_id

class RegisterForm(UserCreationForm):
email = forms.EmailField(
required=True,
label="Gmail",
widget=forms.EmailInput(attrs={'placeholder': 'yourname@gmail.com'})
)
student_id = forms.CharField(
required=True,
max_length=30,
label="Student ID",
widget=forms.TextInput(attrs={'placeholder': 'Enter your Student ID'})
)

class Meta:
model = User
fields = ['username', 'email', 'student_id', 'password1', 'password2']

def __init__(self, *args, **kwargs):
super().__init__(*args, **kwargs)
self.fields['username'].widget.attrs.update({'placeholder': 'Choose Username'})
self.fields['password1'].widget.attrs.update({'placeholder': 'Choose Password'})
self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

def clean_student_id(self):
sid = self.cleaned_data['student_id'].strip().upper()
try:
validate_unima_student_id(sid)
except forms.ValidationError as e:
raise e

if StudentProfile.objects.filter(student_id=sid).exists():
raise forms.ValidationError("This Student ID is already registered.")
return sid

def save(self, commit=True):
user = super().save(commit=False)
user.email = self.cleaned_data['email']
if commit:
user.save()
profile, created = StudentProfile.objects.get_or_create(user=user)
profile.student_id = self.cleaned_data['student_id'].upper()
profile.gmail = self.cleaned_data['email']
profile.save()
return user