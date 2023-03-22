from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from ..models import student_code_valid, User

User: User = get_user_model()

DEFAULT_MAX_LENGTH = 128


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=DEFAULT_MAX_LENGTH, required=True)
    last_name = forms.CharField(max_length=DEFAULT_MAX_LENGTH, required=True)
    password = forms.CharField(
        max_length=DEFAULT_MAX_LENGTH,
        required=True,
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        max_length=DEFAULT_MAX_LENGTH,
        required=True,
        widget=forms.PasswordInput
    )

    def clean(self) -> dict:
        cleaned = super().clean()
        if not (cleaned.get('password') == cleaned.get('confirm_password')):
            raise ValidationError("Passwords must match!")
        return cleaned


class LoginForm(forms.Form):
    student_code: str = forms.CharField(
        max_length=DEFAULT_MAX_LENGTH,
        required=True,
        validators=[student_code_valid]
    )
    password: str = forms.CharField(
        max_length=DEFAULT_MAX_LENGTH,
        required=True,
        widget=forms.PasswordInput
    )

class ManageAccountForm(forms.Form):
    permission_level = forms.CharField(
        max_length=DEFAULT_MAX_LENGTH,
        required=True,
        disabled=True,
        label="User Type"
    )
    first_name = forms.CharField(max_length=DEFAULT_MAX_LENGTH, required=True)
    last_name = forms.CharField(max_length=DEFAULT_MAX_LENGTH, required=True)
    email_address: str = forms.CharField(
        max_length=DEFAULT_MAX_LENGTH,
        required=True,
        disabled=True
    )
