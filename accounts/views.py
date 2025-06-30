from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


# Create your views here.


@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_superuser or user.groups.filter(name="Administrator").exists():
        return redirect("dashboard_admin")
    elif user.groups.filter(name="Author").exists():
        return redirect("dashboard_author")
    elif user.groups.filter(name="Reviewer").exists():
        return redirect("dashboard_reviewer")
    elif user.groups.filter(name="Reader").exists():
        return redirect("dashboard_reader")
    else:
        return redirect("home")  # or some fallback


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


def logout_view(request):
    logout(request)
    return redirect("home")  # Or wherever you want to go after logout


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


# Register a new user and assign them to a default group
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm = request.POST["confirm_password"]

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "accounts/register.html")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        # 🔒 Assign default group
        default_group = Group.objects.get(name="Reader")  # Or 'Author', etc.
        user.groups.add(default_group)

        login(request, user)
        return redirect(
            "dashboard"
        )  # Will route to the correct page via dashboard_redirect

    return render(request, "accounts/register.html")


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
