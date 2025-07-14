from django.shortcuts import render, redirect
from .forms import SubscriberForm
from django.contrib import messages


# Create your views here.


def subscribe(request):
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
    return render(request, "newsletter/thank_you.html")
