from django.shortcuts import render
from django.http import HttpRequest, Http404
from django.views.decorators.http import require_http_methods
from ..models import CourseSession
# TODO: Session management


@require_http_methods(['GET'])
def session_view(request: HttpRequest, session_id: str):
    session_query = CourseSession.objects.filter(pk=session_id)
    if not session_query.exists():
        raise Http404("No session with that ID!")
    return render(
        request,
        'sessions/view.html',
        context={
            'session': session_query.first()
        }
    )