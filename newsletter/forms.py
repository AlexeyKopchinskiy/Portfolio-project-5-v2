from django import forms
from .models import Subscriber
from .models import Newsletter
from django_summernote.widgets import SummernoteWidget


class SubscriberForm(forms.ModelForm):
    """Form for subscribing to the newsletter."""

    class Meta:
        model = Subscriber
        fields = ["email", "name"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your email address",
                    "required": True,
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your name (optional)",
                }
            ),
        }


class NewsletterForm(forms.ModelForm):
    """Form for creating and sending newsletters."""

    class Meta:
        model = Newsletter
        fields = ["subject", "content"]
        widgets = {
            "content": SummernoteWidget(
                attrs={
                    "summernote": {
                        "height": 300,
                        "toolbar": [
                            ["style", ["bold", "italic", "underline"]],
                            ["para", ["ul", "ol"]],
                            ["insert", ["link", "picture"]],
                            ["view", ["fullscreen", "codeview"]],
                        ],
                    }
                }
            )
        }
