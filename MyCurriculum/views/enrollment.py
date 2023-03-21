from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from ..models import Course, UserCourseEnrollment


@require_http_methods(['GET'])
@login_required
def enroll_view(request: HttpRequest, course_code: str):
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that ID!")

    course = course_query.first()
    user = request.user
    enrollment_query = UserCourseEnrollment.objects.filter(
        user=user,
        course=course
    )

    if enrollment_query.exists():
        return HttpResponseRedirect(reverse('MyCurriculum:enroll-summary-view'))

    new_enrollment = UserCourseEnrollment(
        user=user,
        course=course
    )
    new_enrollment.save()
    return HttpResponseRedirect(reverse('MyCurriculum:enroll-summary-view'))


@require_http_methods(['GET'])
@login_required
def unroll_view(request: HttpRequest, course_code: str):
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that ID!")

    course = course_query.first()
    user = request.user

    enrollment_query = UserCourseEnrollment.objects.filter(
        course=course,
        user=user
    )
    if not enrollment_query.exists():
        return HttpResponseRedirect(reverse('MyCurriculum:enroll-summary-view'))

    enrollment = enrollment_query.first()
    enrollment.delete()
    return HttpResponseRedirect(reverse('MyCurriculum:enroll-summary-view'))


@require_http_methods(['GET'])
@login_required
def enroll_summary_view(request: HttpRequest):
    user = request.user
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