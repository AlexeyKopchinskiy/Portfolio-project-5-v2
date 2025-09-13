from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("pricing/", views.pricing, name="pricing"),
    path("cookies/", views.cookies, name="cookies"),
    path("privacy/", views.privacy, name="privacy"),
    path("contact/", views.contact_view, name="contact"),
    # path("sitemap/", views.sitemap, name="sitemap"),
    path(
        "sitemap.xml",
        TemplateView.as_view(
            template_name="sitemap.xml", content_type="application/xml"
        ),
    ),
]
