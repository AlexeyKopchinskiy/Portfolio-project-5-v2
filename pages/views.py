from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from blog.models import Post
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.


def custom_404(request, exception):
    """Render a custom 404 error page."""
    return render(request, "pages/404.html", status=404)


def custom_500(request):
    """Render a custom 500 error page."""
    return render(request, "pages/500.html", status=500)


def home(request):
    """Render the home page with only published posts."""
    latest_posts = Post.objects.filter(is_published=True).order_by(
        "-created_on"
    )[:6]
    return render(request, "pages/home.html", {"latest_posts": latest_posts})


def about(request):
    """Render the about page with general site information."""
    return render(request, "pages/about.html")


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


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
    """Render the pricing page showing available plans or services."""
    return render(request, "pages/pricing.html")


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
