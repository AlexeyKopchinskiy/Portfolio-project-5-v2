from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


# Create your views here.


def dashboard_redirect(request):
    return HttpResponse("Redirecting user based on role...")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # This will redirect based on group
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")


@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_superuser or user.groups.filter(name="Administrator").exists():
        return redirect("dashboard_admin")
    elif user.groups.filter(name="Reviewer").exists():
        return redirect("dashboard_reviewer")
    elif user.groups.filter(name="Author").exists():
        return redirect("dashboard_author")
    elif user.groups.filter(name="Reader").exists():
        return redirect("dashboard_reader")
    else:
        return HttpResponseForbidden(
            "You don't belong to any recognized group."
        )


# # Dashboard views for different user roles
@login_required
def dashboard_reader(request):
    return render(request, "accounts/dashboard_reader.html")


@login_required
def dashboard_author(request):
    return render(request, "accounts/dashboard_author.html")


@login_required
def dashboard_reviewer(request):
    return render(request, "accounts/dashboard_reviewer.html")


@login_required
def dashboard_admin(request):
    return render(request, "accounts/dashboard_admin.html")
