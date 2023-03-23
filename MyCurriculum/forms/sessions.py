from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from .custom_fields import select_datetime


class AddCourseSessionForm(forms.Form):
    start: datetime = select_datetime.SplitDateTimeField(
        required=True
    )

    end: datetime = select_datetime.SplitDateTimeField(
        required=True
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('start') >= cleaned.get('end'):
            raise ValidationError(
                "Start must be before end!"
            )
