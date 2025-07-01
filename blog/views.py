from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by("-published")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "blog/post_detail.html", {"post": post})


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
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("my_posts")
    else:
        form = PostForm(instance=post)
    return render(request, "blog/edit_post.html", {"form": form, "post": post})


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
