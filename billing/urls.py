from django.urls import path
from . import views
# from .views import stripe_webhook


urlpatterns = [
    path("checkout/", views.create_checkout_session, name="checkout"),
    path("success/", views.payment_success, name="payment_success"),
    path("cancel/", views.payment_cancel, name="payment_cancel"),
    # path("webhook/", stripe_webhook, name="stripe-webhook"),
    # path("billing/webhook/", views.stripe_webhook, name="stripe-webhook"),
]
