from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from blog.models import Post, Comment
from newsletter.models import Newsletter
from django.contrib.auth.models import User, Group


# Create your views here.


def custom_404(request, exception):
    """Render a custom 404 error page."""
    return render(request, "pages/404.html", status=404)


def custom_500(request):
    """Render a custom 500 error page."""
    return render(request, "pages/500.html", status=500)


def home(request):
    user = request.user
    is_reader = False
    is_premium = False
    latest_newsletters = None

    """Render the home page with published posts and platform stats."""
    latest_posts = Post.objects.filter(
        is_published=True, premium_post=False
    ).order_by("-created_on")[:6]

    premium_posts = Post.objects.filter(
        is_published=True, premium_post=True
    ).order_by("-published_on")[:3]

    if user.is_authenticated:
        is_reader = user.groups.filter(name="Reader").exists()
        premium_groups = ["Author", "Reviewer", "Administrator"]
        is_premium = user.groups.filter(name__in=premium_groups).exists()

        if is_premium:
            latest_newsletters = Newsletter.objects.order_by("-created_at")[:3]

    newsletter_count = Newsletter.objects.count()

    # Platform statistics
    user_count = User.objects.count()
    group_counts = {
        group.name: group.user_set.count() for group in Group.objects.all()
    }
    post_count = Post.objects.count()
    published_count = Post.objects.filter(is_published=True).count()
    comment_count = Comment.objects.count()

    context = {
        "is_reader": is_reader,
        "latest_posts": latest_posts,
        "user_count": user_count,
        "group_counts": group_counts,
        "post_count": post_count,
        "published_count": published_count,
        "comment_count": comment_count,
        "premium_posts": premium_posts,
        "newsletter_count": newsletter_count,
        "is_premium": is_premium,
        "latest_newsletters": latest_newsletters,
    }

    return render(request, "pages/home.html", context)


def about(request):
    """Render the about page with general site information."""
    return render(request, "pages/about.html")


def contact(request):
    """Handle contact form submission: save to DB only."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the message to the database
            messages.success(
                request,
                "Thanks for reaching out! Your message has been saved.",
            )
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})


def pricing(request):
    user = request.user
    is_premium = False

    if user.is_authenticated:
        premium_groups = ["Author", "Reviewer", "Administrator"]
        is_premium = user.groups.filter(name__in=premium_groups).exists()

    context = {
        "is_premium": is_premium,
    }

    return render(request, "pages/pricing.html", context)


def cookies(request):
    """Render the cookies policy page outlining data usage."""
    return render(request, "pages/cookies.html")


def privacy(request):
    """Render the privacy policy page detailing user data protection."""
    return render(request, "pages/privacy.html")


def sitemap(request):
    """Render the sitemap page for easy navigation."""
    return render(request, "pages/sitemap.html")


def contact_view(request):
    """
    Handle contact form submissions.
    - If GET request, display blank form.
    - If POST request, validate and save the message.
    - Display success message upon successful form submission.
    """

    if request.method == "POST":
        print("Form submitted!")
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thank you! Your message has been received."
            )
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})


def upgrade_required(request):
    return render(request, "pages/upgrade_required.html")
