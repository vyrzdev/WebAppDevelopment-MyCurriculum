from django.shortcuts import render
from django.http import HttpRequest, Http404, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from ..models import Course, CourseAdministrator, CourseSession
from ..forms import ManageCourseForm, AddCourseSessionForm

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
    # Get page number
    try:
        page_number = int(request.GET.get('page', default=0))
    except ValueError:
        page_number = 0

    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that code!")

    course = course_query.first()

    course_session_query = CourseSession.objects.filter(
        course=course
    ).order_by('start')
    return render(
        request,
        'courses/view.html',
        context={
            'course': course,
            'sessions': course_session_query.all()[(page_number*PER_PAGE):((page_number*PER_PAGE)+PER_PAGE)]
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

    if not user.is_superuser:
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
                'course': course,
                'manage_course_form': manage_course_form
            }
        )
    else:
        manage_course_form = ManageCourseForm(request.POST, instance=course)
        if manage_course_form.is_valid():
            manage_course_form.save()
            course.refresh_from_db()  # Just incase!
            return HttpResponseRedirect(f"/course/{course.course_code}")
        else:
            return render(
                request,
                'courses/manage.html',
                context={
                    'course': course,
                    'manage_course_form': manage_course_form
                }
            )


@require_http_methods(['GET', 'POST'])
@login_required
def manage_course_sessions_view(request: HttpRequest, course_code: str):
    # Get page number
    try:
        page_number = int(request.GET.get('page', default=0))
    except ValueError:
        page_number = 0

    user = request.user
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that code!")

    course = course_query.first()

    if not user.is_superuser:
        if not CourseAdministrator.objects.filter(
            user=user,
            course=course
        ).exists():
            raise Http404()

    course_session_query = CourseSession.objects.filter(
        course=course
    )
    return render(
        request,
        'courses/manage_sessions.html',
        context={
            'sessions': course_session_query.all()[(page_number*PER_PAGE):((page_number*PER_PAGE)+PER_PAGE)],
            'next_page': page_number+1,
            'prev_page': page_number-1
        }
    )


@require_http_methods(['GET', 'POST'])
@login_required
def add_course_session_view(request: HttpRequest, course_code: str):
    user = request.user
    course_query = Course.objects.filter(pk=course_code)
    if not course_query.exists():
        raise Http404("No course with that code!")

    course = course_query.first()
    if not user.is_superuser:
        if not CourseAdministrator.objects.filter(
                user=user,
                course=course
        ).exists():
            raise Http404()

    if request.method == "GET":
        add_course_session_form = AddCourseSessionForm()
        return render(
            request,
            'courses/add_session.html',
            context={
                'course': course,
                'add_course_session_form': add_course_session_form
            }
        )
    else:
        add_course_session_form = AddCourseSessionForm(request.POST)
        add_course_session_form.clean()
        cleaned = add_course_session_form.cleaned_data
        if CourseSession.objects.filter(
            course=course,
            end__gte=cleaned.get('start'),
            start__lte=cleaned.get('end')
        ).exists():
            add_course_session_form.add_error(
                field=None,
                error="A CourseSession overlapping this already exists!"
            )
            return render(
                request,
                'courses/add_session.html',
                context={
                    'course': course,
                    'add_course_session_form': add_course_session_form
                }

            )

        new_course_session = CourseSession(
            course=course,
            start=cleaned.get('start'),
            end=cleaned.get('end')
        )

        new_course_session.save()
        return HttpResponseRedirect(f"/course/{course.course_code}")

