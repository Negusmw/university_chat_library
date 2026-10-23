from django.db import models
from django.contrib.auth.models import User

# === FULL UNIMA PROGRAMS ===
PROGRAM_CHOICES = [
    ('BA_CCS', 'BA Communication & Cultural Studies'),
    ('BA_MFD', 'BA Media for Development'),
    ('BA_DRAMA', 'BA Drama & Theatre Studies'),
    ('BA_MUSIC', 'BA Music & Dance'),
    ('BA_FINE_ARTS', 'BA Fine Arts & Design'),
    ('BA_HUMANITIES', 'BA Humanities'),
    ('BA_THEOLOGY', 'BA Theology & Religious Studies'),
    ('BA_PHILOSOPHY', 'BA Philosophy'),
    ('BA_HISTORY', 'BA History & Heritage Studies'),
    ('BA_LINGUISTICS', 'BA Linguistics & Classical Studies'),
    ('BA_LITERARY', 'BA Literary Studies'),
    ('BA_PSYCHOLOGY', 'BA Psychology'),
    ('BA_SOCIOLOGY', 'BA Sociology & Population Studies'),
    ('BA_SOCIAL_WORK', 'BA Social Work'),
    ('BA_GENDER', 'BA Gender Studies'),
    ('LLB', 'Bachelor of Laws (LLB)'),
    ('BA_ECONOMICS', 'BA Economics'),
    ('BA_DEV_ECON', 'BA Development Economics'),
    ('BA_POLITICAL', 'BA Political Science'),
    ('BA_PUBLIC_ADMIN', 'BA Public Administration'),
    ('BEd_LANGUAGE', 'BEd Language'),
    ('BEd_SOCIAL', 'BEd Social Studies'),
    ('BEd_SCIENCE', 'BEd Science'),
    ('BEd_MATHS', 'BEd Mathematics'),
    ('BEd_COMPUTER', 'BEd Computer Science'),
    ('BSc_GENERAL', 'BSc General'),
    ('BSc_BIOLOGY', 'BSc Biological Sciences'),
    ('BSc_CHEMISTRY', 'BSc Chemistry'),
    ('BSc_COMPUTING', 'BSc Computing / Computer Science'),
    ('BSc_MATHS', 'BSc Mathematical Sciences'),
    ('BSc_PHYSICS', 'BSc Physics & Electronics'),
    ('BSc_GEOGRAPHY', 'BSc Geography & Environment'),
    ('BSc_FOOD_NUTRITION', 'BSc Food & Nutrition'),
]

YEAR_CHOICES = [('1','1st Year'),('2','2nd Year'),('3','3rd Year'),('4','4th Year')]

def chat_upload_path(instance, filename):
    return f"chat/{instance.user.username}/{filename}"

class ChatMessage(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('voice', 'Voice Note'),
        ('photo', 'Photo'),
        ('video', 'Video'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    file = models.FileField(upload_to=chat_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    program = models.CharField(max_length=50, choices=PROGRAM_CHOICES, default='BA_PSYCHOLOGY')
    course_code = models.CharField(max_length=20, default='PSY101')
    year = models.CharField(max_length=10, choices=YEAR_CHOICES, default='1')
    file = models.FileField(upload_to='resources/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.program}"

def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        try:
            StudentProfile.objects.get_or_create(user=instance)
        except Exception:
            pass

    def __str__(self):
       return f"{self.user.username} - {self.student_id or 'No ID'}"

# SAFE SIGNAL - never crashes
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.get_or_create(user=instance)
