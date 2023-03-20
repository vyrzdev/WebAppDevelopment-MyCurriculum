from django.shortcuts import render
from django.http import HttpResponse
from ..models import Course


def courses_list_view(request):
    context_dict = {'course_list': Course.objects}
    return render(request, 'courses/course_list.html', context=context_dict)
