from django.http import HttpRequest
from django.shortcuts import render
from ..models import CourseAdministrator, UserCourseEnrollment, Course


def home(request: HttpRequest):
    # TODO: Pagination (VITAL)
    if request.user.is_authenticated:
        course_enrollment_query = UserCourseEnrollment.objects.filter(
            user=request.user
        )

        course_admin_query = CourseAdministrator.objects.filter(
            user=request.user
        )
        return render(
            request,
            'main/homepage.html',
            context={
                'user': request.user,
                'admined_courses': course_admin_query.all(),
                'enrolled_courses': course_enrollment_query.all()
            }
            )

    courses = Course.objects.all()
    return render(
        request,
        'main/homepage.html',
        context={
            'user': request.user,
            'courses': courses
        }
    )