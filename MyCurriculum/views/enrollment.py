from django.http import HttpRequest, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from ..models import Course, UserCourseEnrollment


@login_required
def enroll_view(request: HttpRequest, course_code: str):
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        return Http404("No course with that ID!")

    course = course_query.first()
    user = request.user
    enrollment_query = UserCourseEnrollment.objects.filter(
        user=user,
        course=course
    )

    if enrollment_query.exists():
        return HttpResponse("Enrollment already exists!")

    new_enrollment = UserCourseEnrollment(
        user=user,
        course=course
    )
    new_enrollment.save()
    return HttpResponse("Enrollment Created!")

