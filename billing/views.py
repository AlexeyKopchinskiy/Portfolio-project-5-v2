from django.shortcuts import render, redirect
from decouple import config
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Profile


# Create your views here.
stripe.api_key = config("STRIPE_SECRET_KEY")


import stripe
from django.conf import settings
from django.shortcuts import redirect

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
    endpoint_secret = (
        settings.STRIPE_WEBHOOK_SECRET
    )  # add this to your config vars!

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponseBadRequest()
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # ✅ Now process the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # handle successful checkout — e.g. activate subscription
        print("Checkout complete:", session)

    return HttpResponse(status=200)
