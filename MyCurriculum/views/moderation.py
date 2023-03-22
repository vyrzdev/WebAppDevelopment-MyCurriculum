from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import get_user_model

from ..forms.moderation import CreateCourseForm, CourseAdministratorForm
from ..models import User, Course, CourseAdministrator

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

    return render(
        request,
        'moderation/courses.html',
        context={
            'courses': courses
        }
    )


@require_http_methods(['GET', 'POST'])
@require_admin
def create_course_view(request: HttpRequest):
    if request.method == "GET":
        create_course_form = CreateCourseForm()
        return render(
            request,
            'moderation/create_course.html',
            context={
                'create_course_form': create_course_form
            }
        )
    else:
        create_course_form = CreateCourseForm(request.POST)
        if create_course_form.is_valid():
            create_course_form.save(
                commit=True
            )
            return HttpResponseRedirect("/moderation/courses")
        else:
            return render(
                request,
                'moderation/create_course.html',
                context={
                    'create_course_form': create_course_form
                }
            )


@require_http_methods(['GET'])
@require_admin
def delete_course_view(request: HttpRequest, course_code: str):
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that code!")

    course = course_query.first()
    course.delete()
    return HttpResponseRedirect("/moderation/courses")


@require_http_methods(['GET'])
@require_admin
def manage_course_admins_view(request: HttpRequest, course_code: str):
    # Get page number
    try:
        page_number = int(request.GET.get('page', default=0))
    except ValueError:
        page_number = 0

    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that code!")

    course = course_query.first()
    admin_query = CourseAdministrator.objects.filter(
        course=course
    )
    return render(
        request,
        'moderation/manage_course_admins.html',
        context={
            'course': course,
            'admins': admin_query.all()[(page_number*PER_PAGE):((page_number*PER_PAGE)+PER_PAGE)]
        }
    )


@require_http_methods(['GET', 'POST'])
@require_admin
def add_course_admin_view(request: HttpRequest, course_code: str):
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that code!")
    course = course_query.first()

    if request.method == "GET":
        add_course_admin_form = CourseAdministratorForm()
        return render(
            request,
            'moderation/add_course_admin.html',
            context={
                'add_course_admin_form': add_course_admin_form,
                'course': course
            }
        )
    else:
        add_course_admin_form = CourseAdministratorForm(request.POST)
        if add_course_admin_form.is_valid():
            cleaned = add_course_admin_form.cleaned_data
            user: User = User.objects.filter(pk=cleaned.get('user_code')).first()
            course_administrator_query = CourseAdministrator.objects.filter(
                user=user,
                course=course
            )
            if course_administrator_query.exists():
                add_course_admin_form.add_error("user_code", "User is already an admin of this course!")
                return render(
                    request,
                    'moderation/add_course_admin.html',
                    context={
                        'add_course_admin_form': add_course_admin_form,
                        'course': course
                    }
                )

            new_administrator = CourseAdministrator(
                user=user,
                course=course
            )
            new_administrator.save()
            if (user.permission_level == User.STUDENT):
                user.permission_level = User.ADMIN
                user.save()

            return HttpResponseRedirect(f'/moderation/course/manage_admins/{course.course_code}')
        else:
            return render(
                request,
                'moderation/add_course_admin.html',
                context={
                    'add_course_admin_form': add_course_admin_form,
                    'course': course
                }
            )


@require_http_methods(['GET'])
@require_admin
def remove_course_admin_view(request: HttpRequest, course_code: str, student_code: str):
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that code!")
    course = course_query.first()

    user_query = User.objects.filter(pk=student_code)
    if not user_query.exists():
        raise Http404("No user with that code!")
    user = user_query.first()

    course_admin_query = CourseAdministrator.objects.filter(
        user=user,
        course=course
    )
    if not course_admin_query.exists():
        raise Http404("User is not an admin of this course!")

    course_admin_query.delete()
    return HttpResponseRedirect(f'/moderation/course/manage_admins/{course.course_code}')