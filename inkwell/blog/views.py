from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PostForm
from django.utils.text import slugify
from .models import Post


# Create your views here.


def is_author(user):
    return user.groups.filter(name="Author").exists()


@login_required
# @user_passes_test(lambda u: u.groups.filter(name="Author").exists())
@user_passes_test(
    lambda u: u.groups.filter(name__in=["Author", "Patron"]).exists()
)
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # Generate a unique slug
            base_slug = slugify(post.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug

            post.save()
            form.save_m2m()  # for tags
            messages.success(request, "Your post has been created!")
            return redirect("author_dashboard")
    else:
        form = PostForm()
    return render(request, "author_dashboard/create_post.html", {"form": form})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, "post_details.html", {"post": post})
