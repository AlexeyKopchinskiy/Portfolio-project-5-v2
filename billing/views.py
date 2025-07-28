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


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = "your-endpoint-secret"

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"].get("user_id")

        if user_id:
            user = User.objects.get(id=user_id)
            profile = user.profile  # Or however your user model stores roles
            profile.role = "author"
            profile.save()

    return HttpResponse(status=200)
