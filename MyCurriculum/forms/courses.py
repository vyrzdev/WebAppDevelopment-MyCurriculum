from ..models import Course
from django import forms


class ManageCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'title', 'description']
