from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError


class AccountSettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "location", "avatar"]


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            self.add_error("confirm_password", "Passwords do not match.")
