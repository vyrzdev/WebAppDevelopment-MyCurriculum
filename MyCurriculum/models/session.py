from django.db import models
from django.contrib.admin import ModelAdmin
from .course import Course
import datetime


class CourseSession(models.Model):
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