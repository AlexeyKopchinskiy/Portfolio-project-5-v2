from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Placeholder route to avoid ImproperlyConfigured error
    path("", lambda request: HttpResponse("Accounts app is alive!")),
    # Redirect to dashboard based on user group
    path("", views.dashboard_redirect, name="dashboard"),
    # redirect to specific dashboards based on user group
    path("dashboard/reader/", views.dashboard_reader, name="dashboard_reader"),
    path("dashboard/author/", views.dashboard_author, name="dashboard_author"),
    path(
        "dashboard/reviewer/",
        views.dashboard_reviewer,
        name="dashboard_reviewer",
    ),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    # Register a new user
    path("register/", views.register_view, name="register"),
]
