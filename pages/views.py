from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from blog.models import Post


# Create your views here.


def home(request):
    """Render the home page."""
    # return render(request, "pages/home.html")
    latest_posts = Post.objects.order_by("-created_on")[
        :6
    ]  # adjust count as needed
    return render(request, "pages/home.html", {"latest_posts": latest_posts})


def about(request):
    """Render the about page with general site information."""
    return render(request, "pages/about.html")


def contact(request):
    """Render the static contact page (non-functional version)."""
    return render(request, "pages/contact.html")


def pricing(request):
    """Render the pricing page showing available plans or services."""
    return render(request, "pages/pricing.html")


def cookies(request):
    """Render the cookies policy page outlining data usage."""
    return render(request, "pages/cookies.html")


def privacy(request):
    """Render the privacy policy page detailing user data protection."""
    return render(request, "pages/privacy.html")


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
