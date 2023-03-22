from django import forms
from ..models import Course

DEFAULT_MAX_LENGTH = 128


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'title', 'description']
