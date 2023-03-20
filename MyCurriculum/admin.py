from django.contrib import admin
from .models.user import User, UserAdmin
from .models.course import Course, CourseAdmin
from .models.enrollment import UserCourseEnrollment, UserCourseEnrollmentAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserCourseEnrollment, UserCourseEnrollmentAdmin)
