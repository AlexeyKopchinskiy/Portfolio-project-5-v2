from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.start_page, name="start"),
    path("about/", views.about_page, name="about"),
    path("cookies/", views.cookies_page, name="cookies"),
    path("terms/", views.terms_page, name="terms"),
    path("prices/", views.prices_page, name="prices"),
    path("blog/", include("blog.urls")),
]
