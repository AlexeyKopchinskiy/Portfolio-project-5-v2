from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "featured_image",
            "is_published",
            "reviewer_notes",
            "review_status",
        ]
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
            "reviewer_notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Add internal notes or feedback here...",
                }
            ),
            "review_status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": SummernoteWidget(
                attrs={
                    "summernote": {
                        "toolbar": [
                            ["style", ["bold", "italic"]],
                            ["para", ["ul", "ol"]],
                            ["insert", ["link"]],
                            ["view", ["fullscreen", "codeview"]],
                        ],
                        "height": 120,
                        "disableResizeEditor": True,
                    }
                }
            ),
        }
