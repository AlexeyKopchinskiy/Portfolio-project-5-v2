from django.shortcuts import render, redirect
from decouple import config
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User, Group
from accounts.models import Profile


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


def payment_success(request):
    return render(request, "billing/success.html")


def payment_cancel(request):
    return render(request, "billing/cancel.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("client_reference_id")

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                author_group = Group.objects.get(name="author")
                user.groups.add(author_group)
                logger.info(f"Upgraded user {user.username} to author.")
            except User.DoesNotExist:
                logger.warning(f"User with ID {user_id} not found.")
            except Group.DoesNotExist:
                logger.error("Author group does not exist.")
        else:
            logger.warning("No client_reference_id found in session.")

    return HttpResponse(status=200)
