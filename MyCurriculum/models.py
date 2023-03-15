from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Course(models.Model):
    TITLE_MAX_LENGTH = 128
    DESCRIPTION_MAX_LENGTH = 256

    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(blank=False, max_length=TITLE_MAX_LENGTH)
    code = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.title

class CourseSession(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    location_lat = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)])
    location_long = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)])
    course = models.ForeignKey(Course, blank=False,
                               on_delete=models.CASCADE)
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)

    def __str__(self):
        return self.course.title + " Session " + self.id

class CourseSessionEnrollment(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    session = models.ForeignKey(CourseSession, blank=False,
                                on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name\
            + ": " + str(self.session)

class UserProfile(models.Model):
    STUDENT_CODE_MAX_LENGTH = 8
    # This line is required. Links UserProfile to a User model instance.
    # When the user is deleted, their profile will be deleted as well.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    student_code = models.CharField(blank=False, unique=True,
                                    max_length=STUDENT_CODE_MAX_LENGTH)
    moderator = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.student_code

class ModReport(models.Model):
    STATUS_MAX_LENGTH = 8

    class ModReportStatus(models.TextChoices):
        WAITING = 'WAITING'
        DENIED = 'DENIED'
        RESOLVED = 'RESOLVED'

    id = models.PositiveIntegerField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL)
    status = models.CharField(
        blank=False,
        max_length=STATUS_MAX_LENGTH,
        choices=ModReportStatus.choices,
        default=ModReportStatus.WAITING
    )
    date_created = models.DateTimeField(blank=False)
    date_resolved = models.DateTimeField()
    resolver = models.ForeignKey(User, on_delete=models.SET_NULL)

    def __str__(self):
        return self.creator.first_name + " " + self.creator.last_name\
            + " on " + str(self.date_created)

class Comment(models.Model):
    CONTENT_MAX_LENGTH = 5000

    id = models.PositiveIntegerField(primary_key=True)
    author = models.ForeignKey(User, blank=False,
                               on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, blank=False,
                               on_delete=models.CASCADE)
    content = models.CharField(blank=False,
                               max_length=CONTENT_MAX_LENGTH)
    date_posted = models.DateTimeField(blank=False)

    def __str__(self):
        return self.author.first_name + " " + self.author.last_name\
            + ": " + self.content

class CourseAdminRecord(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    course = models.ForeignKey(Course, blank=False,
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name\
            + ": " + self.course.title
