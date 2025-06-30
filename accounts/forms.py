from django import forms
from django.contrib.auth.models import User
from .models import Profile


class AccountSettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "location", "avatar"]
