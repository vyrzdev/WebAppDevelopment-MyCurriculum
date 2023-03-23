from django.http import HttpRequest, Http404, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from ..models import User
from ..forms import ManageAccountForm

User: User = get_user_model()  # Sneaky type hint magic


@require_http_methods(['GET', 'POST'])
@login_required
def manage_account_view(request: HttpRequest):
    if request.method == "GET":
        form = ManageAccountForm(
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name
            }
        )
        return render(
            request,
            "main/account/manage.html",
            context={
                'form': form
            }
        )
    elif request.method == "POST":
        form = ManageAccountForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            request.user.first_name = cleaned.get('first_name')
            request.user.last_name = cleaned.get('last_name')
            request.user.save()
            return HttpResponseRedirect('/')
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