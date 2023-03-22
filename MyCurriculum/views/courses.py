from django.shortcuts import render
from django.http import HttpRequest, Http404
from django.views.decorators.http import require_http_methods
from ..models import Course

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
