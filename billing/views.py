from django.shortcuts import render, redirect
from decouple import config
import stripe
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User, Group
from accounts.models import Profile
from django.contrib.auth.decorators import login_required


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_checkout_session(request):
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
            success_url="http://localhost:8000/billing/success/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/billing/cancel/",
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


@login_required
def payment_success(request):
    user = request.user
    author_group, _ = Group.objects.get_or_create(name="Author")
    reader_group = Group.objects.get(name="Reader")

    if not user.has_paid_author:
        user.has_paid_author = True
        user.save()

        if user.groups.filter(name="Reader").exists():
            user.groups.remove(reader_group)
            user.groups.add(author_group)
            logger.info(
                f"User {user.username} promoted to Author via success view."
            )
        else:
            logger.info(
                f"User {user.username} already upgraded or not in Reader group."
            )

    return render(request, "billing/success.html")


def payment_cancel(request):
    return render(request, "billing/cancel.html")


logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.error(f"Webhook signature verification failed: {str(e)}")
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("client_reference_id")

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                reader_group = Group.objects.get(name="Reader")
                author_group, _ = Group.objects.get_or_create(name="Author")

                if user.groups.filter(name="Reader").exists():
                    user.groups.remove(reader_group)
                    user.groups.add(author_group)
                    logger.info(
                        f"User {user.username} promoted from Reader to Author via Stripe."
                    )
                else:
                    logger.info(
                        f"User {user.username} is not in Reader group; no promotion applied."
                    )
            except User.DoesNotExist:
                logger.warning(f"User with ID {user_id} not found.")
            except Group.DoesNotExist as e:
                logger.error(f"Group lookup failed: {str(e)}")
        else:
            logger.warning("No client_reference_id found in session.")

    return HttpResponse(status=200)
