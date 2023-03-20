from django.shortcuts import render
from django.http import HttpResponse
from MyCurriculum.models import course

def login(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = pages_list
    context_dict['extra'] = 'From the model solution on GitHub'

    visitor_cookie_handler(request)

    return render(request, 'rango/index.html', context=context_dict)
