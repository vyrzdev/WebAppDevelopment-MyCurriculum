from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from ..models import CourseSession


class AddCourseSessionForm(forms.Form):
    start: datetime = forms.DateTimeField(
        required=True
    )
    end: datetime = forms.DateTimeField(
        required=True
    )
