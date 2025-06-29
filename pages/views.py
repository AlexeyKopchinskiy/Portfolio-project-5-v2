from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact.html")


def pricing(request):
    return render(request, "pages/pricing.html")


def cookies(request):
    return render(request, "pages/cookies.html")


def privacy(request):
    return render(request, "pages/privacy.html")
