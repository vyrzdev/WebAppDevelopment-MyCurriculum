from django import forms
from django.core.exceptions import ValidationError
from ..models import Course, STUDENT_CODE_LENGTH, User
from django.contrib.auth import get_user_model

User: User = get_user_model()

DEFAULT_MAX_LENGTH = 128


def course_exists(course_code: str):
    if not Course.objects.filter(pk=course_code).exists():
        raise ValidationError("No course with this code exists!")


def user_exists(student_code: str):
    if not User.objects.filter(pk=student_code).exists():
        raise ValidationError("No user with this student code exists!")


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'title', 'description']


class CourseAdministratorForm(forms.Form):
    user_code: str = forms.CharField(
        max_length=STUDENT_CODE_LENGTH,
        min_length=STUDENT_CODE_LENGTH,
        required=True,
        validators=[user_exists]
    )