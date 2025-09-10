from django.urls import path, include
from . import views


urlpatterns = [
    path("checkout/", views.create_checkout_session, name="checkout"),
    path("success/", views.payment_success, name="payment_success"),
    path("cancel/", views.payment_cancel, name="payment_cancel"),
]


# Namespace for the billing app
app_name = "billing"
