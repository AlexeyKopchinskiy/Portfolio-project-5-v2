import json
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, Comment
from newsletter.models import Newsletter
from .forms import AccountSettingsForm, ProfileForm
from functools import wraps
from pages.models import ContactMessage


# Create your views here.


# admin views
def is_admin(user):
    return user.is_staff


def role_required(required_group):
    """Decorator to restrict access to users in a specific group."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if (
                not user.is_authenticated
                or not user.groups.filter(name=required_group).exists()
            ):
                return render(request, "pages/access_denied.html", status=403)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


@role_required("Administrator")
def admin_update_users(request):
    """View to update user details by admin."""
    users = User.objects.all()

    # Build user data dictionary
    user_data = {
        str(user.pk): {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
        }
        for user in users
    }

    # Convert to JSON string
    user_data_json = json.dumps(user_data, cls=DjangoJSONEncoder)

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        is_active = request.POST.get("is_active") == "true"
        is_staff = request.POST.get("is_staff") == "true"

        if not all([user_id, first_name, last_name, email]):
            messages.error(request, "⚠️ All fields are required.")
        else:
            user = get_object_or_404(User, pk=user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_active = is_active
            user.is_staff = is_staff
            user.save()
            messages.success(
                request, f"✅ User '{user.username}' updated successfully."
            )
            return redirect("admin_update_users")

    return render(
        request,
        "accounts/admin_update_users.html",
        {
            "users": users,
            "user_data_json": user_data_json,
        },
    )


@role_required("Administrator")
def admin_delete_users(request):
    """View to delete users by admin."""
    users = User.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, pk=user_id)

        if user == request.user:
            messages.error(request, "⚠️ You cannot delete your own account.")
            return redirect("dashboard_admin")

        username = user.username
        user.delete()
        messages.success(
            request, f"🗑️ User '{username}' has been permanently deleted."
        )
        return redirect("dashboard_admin")

    return render(
        request, "accounts/admin_delete_users.html", {"users": users}
    )


@role_required("Administrator")
def admin_change_user_type(request):
    """View to change user roles by admin."""
    users = User.objects.all()
    groups = Group.objects.all()
    # Exclude 'Administrator' group from being assigned
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        new_group_id = request.POST.get("new_type")

        try:
            user = User.objects.get(id=user_id)
            new_group = Group.objects.get(id=new_group_id)

            # Clear existing groups and assign new ones
            user.groups.clear()
            user.groups.add(new_group)

            messages.success(
                request,
                f"{user.username} has been assigned"
                "to the '{new_group.name}' role.",
            )
        except (User.DoesNotExist, Group.DoesNotExist):
            messages.error(request, "Invalid user or role selection.")

        return redirect(
            "dashboard_admin"
        )  # Redirect to admin dashboard after change

    return render(
        request,
        "accounts/admin_change_user_type.html",
        {
            "users": users,
            "groups": groups,
        },
    )


@role_required("Administrator")
def contact_messages_view(request):
    """Display all contact messages to admin users."""
    contact_messages = ContactMessage.objects.all().order_by("-timestamp")
    return render(
        request,
        "accounts/admin_contact_messages.html",
        {"contact_messages": contact_messages},
    )


@role_required("Administrator")
def contact_message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)

    if request.method == "POST":
        resolved = request.POST.get("resolved") == "on"
        message.resolved = resolved
        message.save()
        return redirect("admin_contact_messages")

    return render(
        request, "accounts/contact_message_details.html", {"message": message}
    )


# end of admin views


@login_required
def dashboard_redirect(request):
    """Redirect users to their respective dashboards based on roles."""
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
    """Log out the user and redirect to home."""
    logout(request)
    messages.success(request, "You've been logged out. See you soon!")
    return redirect("home")  # Or wherever you want to go after logout


def register_view(request):
    """Handle user registration."""
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
                "Reader group is missing."
                "Please contact support or an admin to fix this.",
            )
            return redirect("home")

        login(request, user)
        return redirect("dashboard")

    return render(request, "account/signup.html")


# Dashboard views for different user roles
@login_required
def dashboard_reader(request):
    """Dashboard view for Reader role."""
    user = request.user

    recent_comments = Comment.objects.filter(author=user).order_by(
        "-created_at"
    )[:5]
    latest_posts = Post.objects.filter(is_published="True").order_by(
        "-created_on"
    )[:3]

    context = {
        "recent_comments": recent_comments,
        "latest_posts": latest_posts,
    }

    return render(request, "accounts/dashboard_reader.html", context)


@role_required("Author")
def dashboard_author(request):
    """Dashboard view for Author role."""
    user = request.user

    drafts = Newsletter.objects.filter(sent=False).order_by("-created_at")[:5]
    published = Newsletter.objects.filter(sent=True).order_by(
        "-scheduled_send"
    )[:5]

    recent_posts = Post.objects.filter(author__id=user.id).order_by(
        "-created_on"
    )[:5]
    recent_comments = Comment.objects.filter(author=user).order_by(
        "-created_at"
    )[:5]

    context = {
        "drafts": drafts,
        "published": published,
        "recent_posts": recent_posts,
        "recent_comments": recent_comments,
    }

    return render(request, "accounts/dashboard_author.html", context)


@login_required
def dashboard_admin(request):
    """Dashboard view for Admin role."""
    user = request.user

    latest_posts = Post.objects.filter(is_published="True").order_by(
        "-created_on"
    )[:2]

    context = {
        "latest_posts": latest_posts,
    }

    return render(request, "accounts/dashboard_admin.html", context)


@role_required("Reviewer")
def dashboard_reviewer(request):
    """Dashboard view for Reviewer role."""
    unpublished_posts = Post.objects.filter(is_published=False)
    latest_posts = Post.objects.filter(is_published=True).order_by(
        "-created_on"
    )[:5]

    context = {
        "posts": unpublished_posts,
        "latest_posts": latest_posts,
        "dashboard_title": "Reviewer Dashboard",
        "dashboard_description": (
            "Review pending articles and stay updated with recent publications."
        ),
    }

    return render(request, "accounts/dashboard_reviewer.html", context)


@login_required
def account_settings(request):
    """View to handle account settings and profile updates."""
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
    """View to handle password change."""

    template_name = "account/password_change.html"
    success_url = reverse_lazy("password_change_done")


# Password change done view
class PasswordChangeDoneView(TemplateView):
    """View to confirm password change."""

    template_name = "account/password_change_done.html"
