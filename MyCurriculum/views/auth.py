from django.shortcuts import render, reverse
from django.http import HttpRequest, HttpResponseRedirect
from ..forms import RegistrationForm, LoginForm
from ..models import random_student_code, User
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.decorators.http import require_http_methods

User: User = get_user_model()


@require_http_methods(['GET'])
def logout_view(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('MyCurriculum:login-view'))


@require_http_methods(['GET', 'POST'])
def register_view(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("MyCurriculum:course-list-view"))
    if request.method == "GET":
        form = RegistrationForm()
        return render(
            request,
            "auth/register.html",
            context={
                'form': form
            }
        )
    elif request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():

            # Get a random student code.
            valid_code = False
            while not valid_code:
                student_code = random_student_code()
                if not User.objects.filter(pk=student_code).exists():
                    valid_code = True

            # Got valid student code.
            # Now create user!
            cleaned = form.cleaned_data
            user = User.objects.create_user(
                student_code,
                cleaned.get('first_name'),
                cleaned.get('last_name'),
                cleaned.get('password')
            )
            user.save()
            return HttpResponseRedirect(reverse('MyCurriculum:login-view'))
        else:
            return render(
                request,
                "auth/register.html",
                context={
                    'form': form
                }
            )
    else:
        raise RuntimeError("Unexpected Method Type in register view!")


@require_http_methods(['GET', 'POST'])
def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("MyCurriculum:course-list-view"))
    if request.method == "GET":
        form = LoginForm()
        return render(
            request,
            'auth/login.html',
            context={
                'form': form
            }
        )
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            user = authenticate(
                request,
                username=cleaned.get('student_code'),
                password=cleaned.get('password')
            )
            if user is None:
                form.add_error('student_code', 'No users for this username/password combination.')
                return render(
                    request,
                    'auth/login.html',
                    context={
                        'form': form
                    }
                )
            else:
                login(request, user)
                return HttpResponseRedirect(reverse("MyCurriculum:course-list-view"))
        else:
            return render(
                request,
                'auth/login.html',
                context={
                    'form': form
                }
            )
    else:
        raise RuntimeError('Unexpected HTTP method for login_view!')
