from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "featured_image", "is_published"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter post title",
                }
            ),
            "content": SummernoteWidget(),
            "featured_image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "is_published": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
