from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .forms import AccountSettingsForm, ProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from blog.models import Post
from newsletter.models import Newsletter
from .forms import SignUpForm


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


def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out. See you soon!")
    return redirect("home")  # Or wherever you want to go after logout


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")

        # Guard against blank form data
        if not username or not email or not password or not confirm:
            messages.error(request, "Please fill in all required fields.")
            return render(
                request, "account/signup.html", {"form_data": request.POST}
            )

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(
                request, "account/signup.html", {"form_data": request.POST}
            )

        # Validate email format
        if User.objects.filter(email=email).exists():
            messages.error(
                request, "An account with this email already exists."
            )
            return render(
                request, "account/signup.html", {"form_data": request.POST}
            )

        # Validate password confirmation
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(
                request, "account/signup.html", {"form_data": request.POST}
            )

        # Create the user
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        # 🔒 Assign default group
        try:
            default_group = Group.objects.get(name="Reader")
            user.groups.add(default_group)
        except Group.DoesNotExist:
            messages.warning(
                request,
                "Reader group is missing. Please contact support or an admin to fix this.",
            )
            return redirect("home")

        login(request, user)
        return redirect("dashboard")

    return render(request, "account/signup.html")


# # Dashboard views for different user roles
@login_required
def dashboard_reader(request):
    return render(request, "accounts/dashboard_reader.html")


from blog.models import Post  # import from blog app


@login_required
def dashboard_author(request):
    user = request.user

    drafts = Newsletter.objects.filter(sent=False).order_by("-created_at")[:5]
    published = Newsletter.objects.filter(sent=True).order_by(
        "-scheduled_send"
    )[:5]

    # recent_posts = Post.objects.filter(author=user).order_by("-created_at")[:5]
    recent_posts = Post.objects.filter(author__id=request.user.id).order_by(
        "-created_on"
    )[:5]
    # recent_posts = Post.objects.filter(
    #     author__username=request.user.username
    # ).order_by("-created_on")[:5]

    context = {
        "drafts": drafts,
        "published": published,
        "recent_posts": recent_posts,
    }

    return render(request, "accounts/dashboard_author.html", context)


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


@login_required
def dashboard_reviewer(request):
    posts = Post.objects.all()
    return render(
        request,
        "accounts/dashboard_reviewer.html",
        {"posts": posts, "test_flag": "✅ Context works"},
    )
