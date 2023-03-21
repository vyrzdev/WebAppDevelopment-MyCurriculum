from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model
from ..models import User

from typing import Callable

User: User = get_user_model()  # Get user model, and do some sneaky typing magic for autocomplete :)


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