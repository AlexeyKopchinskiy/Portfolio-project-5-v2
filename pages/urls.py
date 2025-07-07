from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("pricing/", views.pricing, name="pricing"),
    path("cookies/", views.cookies, name="cookies"),
    path("privacy/", views.privacy, name="privacy"),
    path("contact/", views.contact_view, name="contact"),
]
