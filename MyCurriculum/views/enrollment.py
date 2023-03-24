from django.http import HttpRequest, Http404, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from ..models import Course, UserCourseEnrollment, User

User: User = get_user_model()  # Sneaky type hint magic


@require_http_methods(['GET'])
@login_required
def enroll_view(request: HttpRequest, course_code: str):
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that ID!")

    course: Course = course_query.first()
    user: User = request.user
    enrollment_query = UserCourseEnrollment.objects.filter(
        user=user,
        course=course
    )

    if enrollment_query.exists():
        return HttpResponseRedirect("/")

    new_enrollment = UserCourseEnrollment(
        user=user,
        course=course
    )
    new_enrollment.save()
    return HttpResponseRedirect("/")


@require_http_methods(['GET'])
@login_required
def unroll_view(request: HttpRequest, course_code: str):
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that ID!")

    course: Course = course_query.first()
    user: User = request.user

    enrollment_query = UserCourseEnrollment.objects.filter(
        course=course,
        user=user
    )
    if not enrollment_query.exists():
        return HttpResponseRedirect("/")

    enrollment: UserCourseEnrollment = enrollment_query.first()
    enrollment.delete()
    return HttpResponseRedirect("/")


@require_http_methods(['GET'])
@login_required
def enroll_summary_view(request: HttpRequest):
    user: User = request.user
    enrollment_query = UserCourseEnrollment.objects.filter(
        user=user
    )
    return render(
        request,
        'enrollment/summary.html',
        context={
            'enrollments': enrollment_query.all()
        }
    )
