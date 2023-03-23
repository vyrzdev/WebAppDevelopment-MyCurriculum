from django.shortcuts import render
from django.http import HttpRequest, Http404, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from ..models import Course, CourseAdministrator, CourseSession, UserCourseEnrollment
from ..forms import ManageCourseForm, AddCourseSessionForm

PER_PAGE = 20


# DONE
@require_http_methods(['GET'])
def course_list_view(request: HttpRequest):
    # Get page number
    try:
        page = int(request.GET.get('page', default=1))
    except ValueError:
        page = 1

    courses_query = Course.objects.order_by('course_code')

    if courses_query.count() > (PER_PAGE*page):
        next_page = page+1
    else:
        next_page = None

    if page > 1:
        previous_page = page-1
    else:
        previous_page = None

    return render(
        request,
        'main/course/list.html',
        context={
            'courses': courses_query.all()[(page-1)*PER_PAGE:(page*PER_PAGE)],
            'next_page': next_page,
            'previous_page': previous_page,
            'current_page': page
        }
    )

# DONE
@require_http_methods(['GET'])
def course_view(request: HttpRequest, course_code: str):
    # Get Page number from URL params
    try:
        page = int(request.GET.get('page', default=1))
    except ValueError:
        page = 1

    # Get course, throw 404 if non existent
    course_query = Course.objects.filter(
        pk=course_code
    )
    if not course_query.exists():
        raise Http404()

    course = course_query.first()

    if request.user.is_authenticated:
        is_enrolled_in_course = UserCourseEnrollment.objects.filter(
            course=course,
            user=request.user
        ).exists()

        is_admin_of_course = CourseAdministrator.objects.filter(
            course=course,
            user=request.user
        ).exists()
    else:
        is_enrolled_in_course = False
        is_admin_of_course = False

    course_session_query = CourseSession.objects.filter(
        course=course
    ).order_by('start')

    session_count = course_session_query.count()
    if session_count > (PER_PAGE * page):
        next_page = page+1
    else:
        next_page = None

    if page > 1:
        previous_page = page - 1
    else:
        previous_page = None

    return render(
        request,
        'main/course/view.html',
        context={
            'course': course,
            'user': request.user,
            'is_enrolled_in_course': is_enrolled_in_course,
            'is_admin_of_course': is_admin_of_course,
            'sessions': course_session_query[((page-1)*PER_PAGE):(page*PER_PAGE)],
            'next_page': next_page,
            'previous_page': previous_page,
            'current_page': page
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
            'course': course,
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
        if add_course_session_form.is_valid():
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
        else:
            return render(
                request,
                'courses/add_session.html',
                context={
                    'course': course,
                    'add_course_session_form': add_course_session_form
                }
            )