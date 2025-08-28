from django.urls import path
from . import views
from .views import my_comments, edit_comment


urlpatterns = [
    path("my-comments/", my_comments, name="my_comments"),
    path("comments/edit/<int:pk>/", views.edit_comment, name="edit_comment"),
    path("create/", views.create_post, name="create_post"),
    path("my-posts/", views.my_posts, name="my_posts"),
    path("", views.post_list, name="post_list"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path("edit/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path(
        "review/edit/<int:post_id>/",
        views.edit_user_post,
        name="edit_user_post",
    ),
]
