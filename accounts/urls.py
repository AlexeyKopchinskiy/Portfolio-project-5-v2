from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    # Placeholder route to avoid ImproperlyConfigured error
    path("", lambda request: HttpResponse("Accounts app is alive!")),
    path("", views.dashboard_redirect, name="dashboard"),
]
