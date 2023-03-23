from django.shortcuts import render
from django.http import HttpRequest, Http404, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from ..models import Course, CourseAdministrator
from ..forms import ManageCourseForm

PER_PAGE = 20


@require_http_methods(['GET'])
def course_list_view(request: HttpRequest):
    # Get page number
    try:
        page_number = int(request.GET.get('page', default=0))
    except ValueError:
        page_number = 0

    # Build queryset.
    courses = Course.objects.all()[(page_number*PER_PAGE):((page_number*PER_PAGE)+PER_PAGE)]

    return render(
        request,
        'courses/list.html',
        context={
            'courses': courses,
            'next_page': page_number+1,
            'prev_page': page_number-1
        }
    )


@require_http_methods(['GET'])
def course_view(request: HttpRequest, course_code: str):
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that code!")

    course = course_query.first()
    return render(
        request,
        'courses/view.html',
        context={
            'course': course
        }
    )


@require_http_methods(['GET', 'POST'])
@login_required
def manage_course_view(request: HttpRequest, course_code: str):
    user = request.user
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that code!")

    course = course_query.first()

    if not user.is_superuser():
        if not CourseAdministrator.objects.filter(
            user=user,
            course=course
        ).exists():
            raise Http404()

    if request.method == "GET":
        manage_course_form = ManageCourseForm(instance=course)
        return render(
            request,
            'courses/manage.html',
            context={
                'manage_course_form': manage_course_form
            }
        )
    else:
        manage_course_form = ManageCourseForm(request.POST, instance=course)
        if manage_course_form.is_valid():
            manage_course_form.save()
            course.refresh_from_db(using=['course_code'])  # Just incase!
            return HttpResponseRedirect(f"/course/{course.course_code}")
        else:
            return render(
                request,
                'courses/manage.html',
                context={
                    'manage_course_form': manage_course_form
                }
            )