from django.shortcuts import render, redirect
import stripe
from decouple import config


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
