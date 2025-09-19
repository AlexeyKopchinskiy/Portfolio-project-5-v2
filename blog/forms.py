from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts."""

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "featured_image",
            "is_published",
            "premium_post",
            "reviewer_notes",
            "review_status",
            "ready",
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
            "premium_post": forms.CheckboxInput(
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
            "ready": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "id": "readyCheckbox",
                }
            ),
        }


class AuthorForm(forms.ModelForm):
    """Form for authors to create and edit their blog posts."""

    class Meta:
        model = Post
        fields = ["title", "content", "featured_image", "ready"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": SummernoteWidget(),
            "featured_image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "ready": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "id": "readyCheckbox",
                }
            ),
        }


class ReviewerForm(forms.ModelForm):
    """Form for reviewers to update review status and notes."""

    class Meta:
        model = Post
        fields = [
            "review_status",
            "reviewer_notes",
            "is_published",
            "premium_post",
            "ready",
        ]
        widgets = {
            "review_status": forms.Select(attrs={"class": "form-control"}),
            "reviewer_notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 6}
            ),
            "is_published": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "premium_post": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "ready": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "id": "readyCheckbox",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    """Form for adding comments to blog posts."""

    class Meta:
        model = Comment
        fields = ["content", "approved"]
        widgets = {
            "content": SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if not user or not user.is_staff:
            self.fields.pop("approved", None)
