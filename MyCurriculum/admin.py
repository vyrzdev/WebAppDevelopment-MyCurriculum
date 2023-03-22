from django.contrib import admin
from .models.user import User, UserAdmin
from .models.course import Course, CourseAdmin
from .models.enrollment import UserCourseEnrollment, UserCourseEnrollmentAdmin
from .models.session import CourseSession, CourseSessionAdmin
from .models.courseadmin import CourseAdministrator, CourseAdministratorAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserCourseEnrollment, UserCourseEnrollmentAdmin)
admin.site.register(CourseSession, CourseSessionAdmin)
admin.site.register(CourseAdministrator, CourseAdministratorAdmin)