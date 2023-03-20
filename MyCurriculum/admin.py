from django.contrib import admin
from .models.user import User, UserAdmin
from .models.course import Course, CourseAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
# Register your models here.
