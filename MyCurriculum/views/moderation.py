from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model

from ..forms.moderation import CreateCourseForm
from ..models import User, Course

from typing import Callable

User: User = get_user_model()  # Get user model, and do some sneaky typing magic for autocomplete :)

PER_PAGE = 20

# Decorator that requires django superuser level.
def require_admin(func: Callable) -> Callable:
    def wrapped(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                raise Http404()
        else:
            raise Http404()
    return wrapped


@require_http_methods(["GET"])
@require_admin
def moderation_index_view(request: HttpRequest):
    # Return simple rendered page.
    return render(
        request,
        'moderation/index.html',
    )


@require_http_methods(["GET"])
@require_admin
def moderation_manage_courses_view(request: HttpRequest):
    # Get page number
    try:
        page_number = int(request.GET.get('page', default=0))
    except ValueError:
        page_number = 0

    # Build queryset.
    courses = Course.objects.all()[(page_number*PER_PAGE):((page_number*PER_PAGE)+PER_PAGE)]


    create_course_form = CreateCourseForm()
    return render(
        request,
        'moderation/courses.html',
        context={
            'create_course_form': create_course_form,
            'courses': courses
        }
    )