from django.db import models
from django.contrib.admin import ModelAdmin
from .user import User
from .course import Course


class UserCourseEnrollment(models.Model):
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


class UserCourseEnrollmentAdmin(ModelAdmin):
    pass
