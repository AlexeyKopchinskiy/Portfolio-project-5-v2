from django.urls import path
from .views import post_detail
from . import views

app_name = "blog"

urlpatterns = [
    # example route
    path("create/", views.create_post, name="create_post"),
    # path("<slug:slug>/", post_detail, name="post_detail"),
    path("<slug:slug>/", post_detail, name="post_detail"),
]
