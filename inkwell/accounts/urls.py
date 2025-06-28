from .views import RoleBasedLoginView
from django.urls import path
from accounts.views import register_reader
from . import views

urlpatterns = [
    path("register/", register_reader, name="register"),
    path("reader/", views.reader_dashboard, name="reader_dashboard"),
    path("author/", views.author_dashboard, name="author_dashboard"),
    path("patron/", views.patron_dashboard, name="patron_dashboard"),
    path("logout/", views.custom_logout, name="logout"),
    path(
        "login/",
        RoleBasedLoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
]
