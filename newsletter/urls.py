from django.urls import path
from . import views

urlpatterns = [
    path("subscribe/", views.subscribe, name="newsletter_subscribe"),
    path("thank-you/", views.thank_you, name="newsletter_thank_you"),
]
