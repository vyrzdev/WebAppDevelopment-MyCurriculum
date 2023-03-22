from django.urls import path
from . import views

app_name = "MyCurriculum"

urlpatterns = [
    # Authentication//Authorisation views
    path("auth/register", views.auth.register_view, name='register-view'),
    path("auth/login", views.auth.login_view, name='login-view'),
    path("auth/logout", views.auth.logout_view, name='logout-view'),
    # Course Views
    path("courses", views.courses.course_list_view, name="course-list-view"),
    path("course/<str:course_code>", views.courses.course_view, name="course-view"),
    # Enrollment Views
    path("enroll/<str:course_code>", views.enrollment.enroll_view, name='enroll-view'),
    path("unroll/<str:course_code>", views.enrollment.unroll_view, name='unroll-view'),
    path("enrollments", views.enrollment.enroll_summary_view, name='enroll-summary-view'),
    # Account Views
    path("account", views.account.manage_account_view, name='manage-account-view'),
    path("moderation", views.moderation.moderation_index_view, name='moderation-index-view'),
    path("moderation/courses", views.moderation.moderation_manage_courses_view, name="moderation-manage-courses-view"),
    path("moderation/courses/create", views.moderation.create_course_view, name="moderation-create-course-view"),
    path("moderation/courses/delete/<str:course_code>", views.moderation.delete_course_view, name="moderation-delete-course-view"),
    path("moderation/course/manage_admins/<str:course_code>", views.moderation.manage_course_admins_view, name="moderation-manage-course-admins-view"),
    path("moderation/course/add_admin/<str:course_code>", views.moderation.add_course_admin_view, name="moderation-add-course-admin-view"),
    path("moderation/course/remove_admin/<str:course_code>/<str:student_code>", views.moderation.remove_course_admin_view, name="moderation-remove-course-admin-view")
]