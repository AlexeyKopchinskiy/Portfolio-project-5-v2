from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by("-published")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "blog/post_detail.html", {"post": post})
