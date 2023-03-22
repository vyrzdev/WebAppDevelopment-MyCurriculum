from django.http import HttpRequest, Http404, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from ..models import User
from ..forms import ManageAccountForm

User: User = get_user_model()  # Sneaky type hint magic


@require_http_methods(['GET'])
@login_required
def manage_account_view(request: HttpRequest):
    if request.method == "GET":
        form = ManageAccountForm()
        return render(
            request,
            "account/account.html",
            context={
                'form': form
            }
        )
    elif request.method == "POST":
        form = ManageAccountForm(request.POST)
        if form.is_valid():
            # Create ModMail with details of name/profile picture change
            # TODO: Fix this shit; Probably allow user to edit name, and password alone
            # and don't allow user to edit permission level at all.
            # TODO: Add profile-picture support
            return HttpResponseRedirect(reverse('MyCurriculum:manage-account-view'))
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