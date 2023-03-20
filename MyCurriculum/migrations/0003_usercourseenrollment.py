# Generated by Django 4.1.7 on 2023-03-20 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyCurriculum', '0002_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='MyCurriculum.course')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
