from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import SubscriberForm, NewsletterForm
from .models import Newsletter, Subscriber


# Create your views here.


def subscribe(request):
    """Handle newsletter subscription."""
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "You're subscribed! Welcome to Inkwell Updates."
            )
            return redirect("newsletter_thank_you")
    else:
        form = SubscriberForm()
    return render(request, "newsletter/subscribe.html", {"form": form})


def thank_you(request):
    """Thank you page after subscribing."""
    return render(request, "newsletter/thank_you.html")


@login_required
def newsletter_dashboard(request):
    """Dashboard for managing newsletters and subscribers."""
    newsletters = Newsletter.objects.all().order_by("-created_at")
    subscribers = Subscriber.objects.all()
    return render(
        request,
        "newsletter/dashboard.html",
        {
            "newsletters": newsletters,
            "subscribers": subscribers,
        },
    )


@login_required
def create_newsletter(request):
    """Create a new newsletter."""
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            return redirect("newsletter_dashboard")
    else:
        form = NewsletterForm()
    return render(request, "newsletter/create_newsletter.html", {"form": form})


@login_required
def edit_newsletter(request, pk):
    """Edit an existing newsletter."""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            return redirect("newsletter_dashboard")
    else:
        form = NewsletterForm(instance=newsletter)
    return render(
        request,
        "newsletter/edit_newsletter.html",
        {"form": form, "newsletter": newsletter},
    )


@login_required
def view_newsletter(request, pk):
    """View a specific newsletter."""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(
        request, "newsletter/view_newsletter.html", {"newsletter": newsletter}
    )
