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


def create_checkout_session(request):
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
        success_url="http://localhost:8000/billing/success/",
        cancel_url="http://localhost:8000/billing/cancel/",
        metadata={
            "user_id": request.user.id  # 👈 Include user ID for webhook linking
        },
    )
    return redirect(session.url, code=303)


def payment_success(request):
    return render(request, "billing/success.html")


def payment_cancel(request):
    return render(request, "billing/cancel.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]

        try:
            user = User.objects.get(id=user_id)
            author_group = Group.objects.get(
                name="Author"
            )  # ✅ your existing group
            user.groups.add(author_group)
            logger.info(f"User {user.username} added to Author group.")
        except (User.DoesNotExist, Group.DoesNotExist):
            logger.warning("Could not find user or group to apply upgrade.")

    return HttpResponse(status=200)
