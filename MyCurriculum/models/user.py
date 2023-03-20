import random

from django.contrib import admin
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from typing import List, Optional

DEFAULT_MAX_LENGTH: int = 128
STUDENT_CODE_LENGTH: int = 8
STUDENT_CODE_SUFFIXES: List[str] = ['A', 'B', 'C']


# Validates student code.
def student_code_valid(student_code: str):
    if not (
        (len(student_code) == STUDENT_CODE_LENGTH)
        and (student_code[-1] in STUDENT_CODE_SUFFIXES)
        and (False not in [x.isdigit() for x in student_code[0:(STUDENT_CODE_LENGTH-1)]])
    ):
        raise ValidationError("Student Code is Invalid!")


# Produces student code of format:
# =================================
# 1234567X
# <-----> STUDENT_CODE_LENGTH randint.
# X in STUDENT_CODE_SUFFIXES
def random_student_code() -> str:
    return (
        str(
            random.randint(0, (
                    10**(STUDENT_CODE_LENGTH-2)-1
            ))
        ).zfill(STUDENT_CODE_LENGTH-1)
        + STUDENT_CODE_SUFFIXES[random.randint(0, len(STUDENT_CODE_SUFFIXES)-1)]
    )


# User AdminModel
# ==================
class UserAdmin(admin.ModelAdmin):
    pass


# User Manager
# =================
class UserManager(BaseUserManager):
    def create_user(
            self,
            student_code: str,
            first_name: str,
            last_name: str,
            password: Optional[str] = None
    ) -> 'User':
        user = User(
            student_code=student_code,
            first_name=first_name,
            last_name=last_name,
            permission_level=User.STUDENT
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self,
            student_code: str,
            first_name: str,
            last_name: str,
            password: Optional[str] = None
    ) -> 'User':
        user = User(
            student_code=student_code,
            first_name=first_name,
            last_name=last_name,
            permission_level=User.ADMIN
        )
        user.set_password(password)
        user.save()
        return user


# User Model
# =====================
class User(AbstractBaseUser):
    # User Fields
    # ====================
    student_code: str = models.CharField(
        primary_key=True,
        max_length=STUDENT_CODE_LENGTH,
        unique=True,
        blank=False,
        editable=False,
        validators=[student_code_valid]
    )

    first_name: str = models.CharField(
        primary_key=False,
        max_length=DEFAULT_MAX_LENGTH,
        unique=False,
        blank=False,
        editable=True
    )

    last_name: str = models.CharField(
        primary_key=False,
        max_length=DEFAULT_MAX_LENGTH,
        unique=False,
        blank=False,
        editable=True
    )

    # Choices Enum
    STUDENT = 'student'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    PERMISSION_LEVEL_CHOICES = [
        (STUDENT, "Student"),
        (MODERATOR, "Moderator"),
        (ADMIN, "Admin")
    ]

    permission_level: str = models.CharField(
        primary_key=False,
        max_length=DEFAULT_MAX_LENGTH,
        choices=PERMISSION_LEVEL_CHOICES,
        unique=False,
        blank=False,
        default=STUDENT
    )

    # Getters
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self) -> str:
        return self.first_name

    @property
    def is_staff(self) -> bool:
        return (self.permission_level in [User.MODERATOR, User.ADMIN])
    
    @property
    def is_superuser(self) -> bool:
        return self.permission_level == User.ADMIN

    # Permissions System
    # TODO: Implement.
    def has_perm(self, *args, **kwargs):
        return True

    def has_module_perms(self, *args, **kwargs):
        return True

    USERNAME_FIELD = 'student_code'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects: UserManager = UserManager()
