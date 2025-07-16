from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm


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


@login_required
def edit_post(request, post_id):
    user = request.user

    # 🕵️ Reviewer check
    is_reviewer = user.groups.filter(name="Reviewer").exists()

    if is_reviewer:
        post = get_object_or_404(Post, id=post_id)
    else:
        # Non-reviewers can only edit their own posts
        post = get_object_or_404(Post, id=post_id, author=user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("my_posts")
    else:
        form = PostForm(instance=post)

    return render(request, "blog/edit_post.html", {"form": form, "post": post})


@login_required
def edit_user_post(request, post_id):
    """
    View for reviewers to edit any user's blog post.

    Only accessible to authenticated users who belong to the 'Reviewer' group.
    Fetches the post by its ID and renders a reviewer-specific editing template.
    Allows review actions, post modification, and form submission handling.

    Args:
        request (HttpRequest): The incoming HTTP request.
        post_id (int): The ID of the post to be reviewed and potentially edited.

    Returns:
        HttpResponse: Renders the reviewer's editing page with the form and post data,
                      or redirects upon successful update.
        HttpResponseForbidden: If the user is not a reviewer.
    """

    user = request.user

    # Ensure only reviewers access this view
    if not user.groups.filter(name="Reviewer").exists():
        return HttpResponseForbidden("Access denied.")

    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(
            "dashboard_reviewer"
        )  # Update this to your actual dashboard view name

    return render(
        request, "blog/edit_user_post.html", {"form": form, "post": post}
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
