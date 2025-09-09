from django.urls import path
from .views import CustomPasswordChangeView, PasswordChangeDoneView
from . import views


urlpatterns = [
    # path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Redirect to dashboard based on user group
    path("", views.dashboard_redirect, name="dashboard"),
    # redirect to specific dashboards based on user group
    path("redirect/", views.dashboard_redirect, name="role_redirect"),
    path("dashboard/reader/", views.dashboard_reader, name="dashboard_reader"),
    path("dashboard/author/", views.dashboard_author, name="dashboard_author"),
    path(
        "dashboard/reviewer/",
        views.dashboard_reviewer,
        name="dashboard_reviewer",
    ),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path(
        "dashboard/admin/update-users/",
        views.admin_update_users,
        name="admin_update_users",
    ),
    path(
        "dashboard/admin/delete-users/",
        views.admin_delete_users,
        name="admin_delete_users",
    ),
    path(
        "dashboard/admin/change-user-type/",
        views.admin_change_user_type,
        name="admin_change_user_type",
    ),
    path(
        "dashboard/admin/contact-messages/",
        views.contact_messages_view,
        name="admin_contact_messages",
    ),
    path(
        "admin/contact-messages/<int:pk>/",
        views.contact_message_detail,
        name="contact_message_detail",
    ),
    # Register a new user
    path("register/", views.register_view, name="register"),
    # Account settings
    path("settings/", views.account_settings, name="account_settings"),
    # Password change views
    path(
        "change-password/",
        CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    # Password change done view
    path(
        "change-password/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "guidelines/reviewers/",
        views.guidelines_for_reviewers,
        name="guidelines_for_reviewers",
    ),
]
