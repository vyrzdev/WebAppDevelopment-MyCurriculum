from django.db import models
from django.contrib.admin import ModelAdmin
from .course import Course
import datetime
import uuid


class CourseSession(models.Model):
    session_id: str = models.CharField(
        primary_key=True,
        unique=True,
        blank=False,
        editable=False,
        max_length=64
    )

    course: Course = models.ForeignKey(
        Course,
        primary_key=False,
        unique=False,
        blank=False,
        editable=False,
        on_delete=models.CASCADE
    )

    # TODO: Location.
    start: datetime.datetime = models.DateTimeField(
        primary_key=False,
        unique=False,
        blank=False,
        editable=True,
    )
    end: datetime.datetime = models.DateTimeField(
        primary_key=False,
        unique=False,
        blank=False,
        editable=True,
    )


class CourseSessionAdmin(ModelAdmin):
    pass