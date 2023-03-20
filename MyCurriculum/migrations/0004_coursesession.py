# Generated by Django 4.1.7 on 2023-03-20 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyCurriculum', '0003_usercourseenrollment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('course', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='MyCurriculum.course')),
            ],
        ),
    ]
