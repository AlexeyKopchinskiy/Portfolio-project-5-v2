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
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("my_posts")


@login_required
def edit_user_post(request, post_id):
    user = request.user

    post = get_object_or_404(Post, id=post_id)

    # Ensure only reviewers access this view
    if not user.groups.filter(name="Reviewer").exists():
        return HttpResponseForbidden("Access denied.")

    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    # Disable reviewer-only fields if the user is the author
    if user == post.author:
        form.fields["review_status"].disabled = True
        form.fields["reviewer_notes"].disabled = True

    if request.method == "POST" and form.is_valid():
        # Prevent authors from modifying reviewer-only fields
        if user == post.author:
            form.cleaned_data["review_status"] = post.review_status
            form.cleaned_data["reviewer_notes"] = post.reviewer_notes

        form.save()
        return redirect("dashboard_reviewer")

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
