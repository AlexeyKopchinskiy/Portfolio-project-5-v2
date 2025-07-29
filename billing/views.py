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


def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": "your_stripe_price_id",
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri("/billing/success/"),
        cancel_url=request.build_absolute_uri("/billing/cancel/"),
        metadata={
            "user_id": request.user.id  # 👈 So you can identify the user in the webhook
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
