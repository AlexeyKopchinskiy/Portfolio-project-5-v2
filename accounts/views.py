from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .forms import AccountSettingsForm, ProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView


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
    if request.user.is_authenticated:
        return redirect("dashboard")

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


# Register a new user and assign them to a default group
def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

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


@login_required
def account_settings(request):
    user = request.user

    if request.method == "POST":
        user_form = AccountSettingsForm(request.POST, instance=user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("dashboard")  # Or show a success message
    else:
        user_form = AccountSettingsForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/settings.html", context)


# Custom password change view
class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("password_change_done")


# Password change done view
class PasswordChangeDoneView(TemplateView):
    template_name = "accounts/password_change_done.html"
