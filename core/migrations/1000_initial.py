import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True)),
                ('message_type', models.CharField(choices=[('text', 'Text'), ('voice', 'Voice Note'), ('photo', 'Photo'), ('video', 'Video')], default='text', max_length=10)),
                ('file', models.FileField(blank=True, null=True, upload_to='chat/%(username)s/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('program', models.CharField(choices=[('BA_CCS', 'BA Communication & Cultural Studies'), ('BA_MFD', 'BA Media for Development'), ('BA_DRAMA', 'BA Drama & Theatre Studies'), ('BA_MUSIC', 'BA Music & Dance'), ('BA_FINE_ARTS', 'BA Fine Arts & Design'), ('BA_HUMANITIES', 'BA Humanities'), ('BA_THEOLOGY', 'BA Theology & Religious Studies'), ('BA_PHILOSOPHY', 'BA Philosophy'), ('BA_HISTORY', 'BA History & Heritage Studies'), ('BA_LINGUISTICS', 'BA Linguistics & Classical Studies'), ('BA_LITERARY', 'BA Literary Studies'), ('BA_PSYCHOLOGY', 'BA Psychology'), ('BA_SOCIOLOGY', 'BA Sociology & Population Studies'), ('BA_SOCIAL_WORK', 'BA Social Work'), ('BA_GENDER', 'BA Gender Studies'), ('LLB', 'Bachelor of Laws (LLB)'), ('BA_ECONOMICS', 'BA Economics'), ('BA_DEV_ECON', 'BA Development Economics'), ('BA_POLITICAL', 'BA Political Science'), ('BA_PUBLIC_ADMIN', 'BA Public Administration'), ('BEd_LANGUAGE', 'BEd Language'), ('BEd_SOCIAL', 'BEd Social Studies'), ('BEd_SCIENCE', 'BEd Science'), ('BEd_MATHS', 'BEd Mathematics'), ('BEd_COMPUTER', 'BEd Computer Science'), ('BSc_GENERAL', 'BSc General'), ('BSc_BIOLOGY', 'BSc Biological Sciences'), ('BSc_CHEMISTRY', 'BSc Chemistry'), ('BSc_COMPUTING', 'BSc Computing / Computer Science'), ('BSc_MATHS', 'BSc Mathematical Sciences'), ('BSc_PHYSICS', 'BSc Physics & Electronics'), ('BSc_GEOGRAPHY', 'BSc Geography & Environment'), ('BSc_FOOD_NUTRITION', 'BSc Food & Nutrition')], default='BA_PSYCHOLOGY', max_length=50)),
                ('course_code', models.CharField(default='PSY101', max_length=20)),
                ('year', models.CharField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')], default='1', max_length=10)),
                ('file', models.FileField(upload_to='resources/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(blank=True, default=None, max_length=30, null=True, unique=True)),
                ('gmail', models.EmailField(blank=True, max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
