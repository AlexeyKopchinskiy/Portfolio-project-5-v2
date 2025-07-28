from django.shortcuts import render, redirect
from decouple import config
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from accounts.models import Profile


# Create your views here.
stripe.api_key = config("STRIPE_SECRET_KEY")


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
    )
    return redirect(session.url)


def payment_success(request):
    return render(request, "billing/success.html")


def payment_cancel(request):
    return render(request, "billing/cancel.html")


import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import (
    User,
)  # adjust if using custom user model


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = "your-endpoint-secret"  # replace with your actual Stripe webhook secret

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("metadata", {}).get("user_id")

        if not user_id:
            return HttpResponse(status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        profile = user.profile  # adjust if you store roles elsewhere
        profile.role = "author"
        profile.save()

        # Optional: email or logging
        # send_mail("Account upgraded", "Your account now has author access.", "noreply@yourapp.com", [user.email])
        # logging.info(f"Upgraded user {user.id} to author role")

    return HttpResponse(status=200)
