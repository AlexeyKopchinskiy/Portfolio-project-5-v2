from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Form for the contact page."""

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }
