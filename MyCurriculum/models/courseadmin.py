from .course import Course
from django.contrib.auth import get_user_model
from django.contrib.admin import ModelAdmin
from django.db import models
from .user import User

User: User = get_user_model()


class CourseAdministrator(models.Model):
    user: User = models.ForeignKey(
        User,
        primary_key=False,
        unique=False,
        blank=False,
        editable=False,
        on_delete=models.CASCADE
    )

    course: Course = models.ForeignKey(
        Course,
        primary_key=False,
        unique=False,
        blank=False,
        editable=False,
        on_delete=models.CASCADE
    )


class CourseAdministratorAdmin(ModelAdmin):
    pass
