from django.urls import path
from . import views

urlpatterns = [
    path("auth/register", views.auth.register_view, name='register-view'),
    path("auth/login", views.auth.login_view, name='login-view'),
    path("auth/logout", views.auth.logout_view, name='logout-view'),
    path("enroll/<str:course_code>", views.enrollment.enroll_view, name='enroll-view'),
    path("courses/course-list", views.courses.course_list_view, name="course-list-view"),
]