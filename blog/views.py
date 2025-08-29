from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm, AuthorForm, ReviewerForm


# Create your views here.


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by("-published")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.order_by("-created_at")
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", slug=post.slug)

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
        },
    )


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("my_posts")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, "blog/my_posts.html", {"posts": posts})


# @login_required
# def edit_post(request, post_id):
#     user = request.user

#     # 🕵️ Reviewer check
#     is_reviewer = user.groups.filter(name="Reviewer").exists()

#     if is_reviewer:
#         post = get_object_or_404(Post, id=post_id)
#     else:
#         # Non-reviewers can only edit their own posts
#         post = get_object_or_404(Post, id=post_id, author=user)

#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect("my_posts")
#     else:
#         form = PostForm(instance=post)

#     return render(request, "blog/edit_post.html", {"form": form, "post": post})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author:
        form_class = AuthorForm
    elif (
        request.user.is_staff
        or request.user.groups.filter(name="Reviewers").exists()
    ):
        form_class = ReviewerForm
    else:
        return HttpResponseForbidden(
            "You don't have permission to edit this post."
        )

    form = form_class(
        request.POST or None, request.FILES or None, instance=post
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard")

    return render(
        request,
        "blog/edit_user_post.html",
        {
            "form": form,
            "post": post,
        },
    )


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("my_posts")


@login_required
def edit_user_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Determine which form to use
    if user == post.author:
        form_class = AuthorForm
    elif user.groups.filter(name="Reviewer").exists():
        form_class = ReviewerForm
    else:
        return HttpResponseForbidden(
            "You don't have permission to edit this post."
        )

    form = form_class(
        request.POST or None, request.FILES or None, instance=post
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(
            "dashboard_author" if user == post.author else "dashboard_reviewer"
        )

    return render(
        request,
        "blog/edit_user_post.html",
        {
            "form": form,
            "post": post,
            "user": user,
        },
    )


def is_reviewer(user):
    return user.groups.filter(name="Reviewer").exists()


@login_required
@user_passes_test(is_reviewer)
def review_user_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = ReviewerPostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("reviewer_dashboard")
    return render(
        request, "review_user_post.html", {"form": form, "post": post}
    )


@login_required
def dashboard(request):
    latest_posts = Post.objects.filter(is_published=True).order_by(
        "-published"
    )[:5]
    return render(
        request,
        "accounts/dashboard_author.html",
        {"latest_posts": latest_posts},
    )


@login_required
def my_comments(request):
    user_comments = Comment.objects.filter(author=request.user).order_by(
        "-created_at"
    )
    return render(
        request, "blog/my_comments.html", {"comments": user_comments}
    )


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("my_comments")  # or wherever you list comments
    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        "blog/edit_my_comments.html",
        {"form": form, "comment": comment},
    )


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden(
            "You can't delete someone else's comment."
        )
    comment.delete()
    return redirect("my_comments")
