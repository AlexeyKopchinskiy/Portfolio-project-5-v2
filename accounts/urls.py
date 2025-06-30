from django.urls import path
from django.views.generic import TemplateView
from .views import CustomPasswordChangeView, PasswordChangeDoneView
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
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
    # Account settings
    path("settings/", views.account_settings, name="account_settings"),
    # Password change views
    path(
        "change-password/",
        CustomPasswordChangeView.as_view(),
        name="change_password",
    ),
    # Password change done view
    path(
        "change-password/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
