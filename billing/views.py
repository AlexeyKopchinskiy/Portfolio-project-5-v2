from django.shortcuts import render, redirect
import stripe
import logging
from django.conf import settings
from django.contrib.auth.models import Group
from accounts.models import Profile
from django.contrib.auth.decorators import login_required


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_checkout_session(request):
    """
    Create a Stripe Checkout session and redirect to Stripe's hosted page.
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Demo Product"},
                        "unit_amount": 1200,  # $12.00
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=(
                f"{settings.DOMAIN_URL}/billing/success/"
                f"?session_id={{CHECKOUT_SESSION_ID}}"
            ),
            cancel_url=f"{settings.DOMAIN_URL}/billing/cancel/",
            client_reference_id=str(
                request.user.id
            ),  # ✅ Stripe will send this in webhook
            metadata={
                "user_id": str(
                    request.user.id
                )  # Optional, but useful for debugging
            },
        )
        return redirect(session.url, code=303)
    except Exception as e:
        logger.error(f"Stripe session creation failed: {str(e)}")
        return redirect("billing:error")  # Or show a friendly error page


logger = logging.getLogger(__name__)


@login_required
def payment_success(request):
    """Handle post-payment success logic."""
    user = request.user
    author_group, _ = Group.objects.get_or_create(name="Author")
    reader_group = Group.objects.get(name="Reader")

    # Ensure the user has a profile
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if not profile.has_paid_author:
        profile.has_paid_author = True
        profile.save()

        if user.groups.filter(name="Reader").exists():
            user.groups.remove(reader_group)
            user.groups.add(author_group)
            logger.info(
                f"User {user.username} promoted to Author via success view."
            )
        else:
            logger.info(
                (
                    f"User {user.username} already upgraded "
                    "or not in Reader group."
                )
            )

    return render(request, "billing/success.html")


def payment_cancel(request):
    """Render the payment cancellation page."""
    return render(request, "billing/cancel.html")
