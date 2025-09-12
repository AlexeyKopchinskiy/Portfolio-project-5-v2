from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("premium/", views.premium_post_list, name="premium_post_list"),
    path("my-comments/", views.my_comments, name="my_comments"),
    path("comments/edit/<int:pk>/", views.edit_comment, name="edit_comment"),
    path(
        "comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"
    ),
    path("create/", views.create_post, name="create_post"),
    path("my-posts/", views.my_posts, name="my_posts"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path("edit/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:id>/delete/", views.delete_post, name="delete_post"),
    path(
        "author/edit/<int:post_id>/",
        views.edit_user_post,
        name="edit_user_post",
    ),
    path(
        "review/edit/<int:post_id>/",
        views.review_user_post,
        name="review_user_post",
    ),
    path(
        "moderate/comments/", views.approve_comments, name="approve_comments"
    ),
    path(
        "admin/manage-posts/",
        views.admin_manage_posts,
        name="admin_manage_posts",
    ),
    path(
        "admin/edit-post/<int:post_id>/",
        views.admin_edit_post,
        name="admin_edit_post",
    ),
    path(
        "premium/<slug:slug>/",
        views.premium_post_detail,
        name="premium_post_detail",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
