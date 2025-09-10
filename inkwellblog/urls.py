"""
URL configuration for inkwellblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = "pages.views.custom_404"
handler500 = "pages.views.custom_500"

urlpatterns = [
    path("", include("pages.urls")),
    path("admin/", admin.site.urls),
    path(
        "profile/", include("accounts.urls")
    ),  # <-- This connects to the settings page
    path("accounts/", include("allauth.urls")),  # Allauth still lives here too
    path("blog/", include("blog.urls")),
    path("summernote/", include("django_summernote.urls")),
    path(
        "newsletter/", include("newsletter.urls")
    ),  # <-- This connects newsletter app
    path(
        "billing/", include(("billing.urls", "billing"), namespace="billing")
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
