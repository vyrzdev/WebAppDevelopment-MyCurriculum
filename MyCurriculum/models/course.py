import random

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.admin import ModelAdmin

COURSE_CODE_LENGTH = 5
COURSE_PREFIXES = ['CS']


def course_code_valid(course_code: str):
    if not (course_code[0:2] in COURSE_PREFIXES):
        raise ValidationError("Course code must start with a valid Course Prefix!")
    if len(course_code) != COURSE_CODE_LENGTH:
        raise ValidationError(f"Course code must be of length: {COURSE_CODE_LENGTH}")


# Returns randomized course code of format:
# XX123
#   <-> COURSE_CODE_LENGTH-2 randint.
# XX in COURSE_PREFIXES
def random_course_code() -> str:
    return (
            COURSE_PREFIXES[random.randint(0, len(COURSE_PREFIXES)-1)]
            + str(
                random.randint(0, (10**(COURSE_CODE_LENGTH-1)-1))
            ).zfill(COURSE_CODE_LENGTH-2)
    )


DEFAULT_MAX_LENGTH = 128


class Course(models.Model):
    course_code: str = models.CharField(
        primary_key=True,
        max_length=COURSE_CODE_LENGTH,
        unique=True,
        blank=False,
        editable=True,
        validators=[course_code_valid]
    )

    title: str = models.CharField(
        primary_key=False,
        max_length=DEFAULT_MAX_LENGTH,
        unique=False,
        blank=False,
        editable=True,
    )

    description: str = models.TextField(
        primary_key=False,
        editable=True,
        unique=False,
        blank=False
    )

    # TODO: Implement Scores.
    @property
    def score(self) -> int:
        return 100

class CourseAdmin(ModelAdmin):
    pass