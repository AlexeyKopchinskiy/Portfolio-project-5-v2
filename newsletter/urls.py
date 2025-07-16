from django.urls import path
from . import views
from .views import (
    newsletter_dashboard,
    create_newsletter,
    edit_newsletter,
    view_newsletter,
)


urlpatterns = [
    path("dashboard/", newsletter_dashboard, name="newsletter_dashboard"),
    path("create/", create_newsletter, name="create_newsletter"),
    path("<int:pk>/edit/", edit_newsletter, name="edit_newsletter"),
    path("<int:pk>/view/", view_newsletter, name="view_newsletter"),
    path("subscribe/", views.subscribe, name="newsletter_subscribe"),
    path("thank-you/", views.thank_you, name="newsletter_thank_you"),
]
