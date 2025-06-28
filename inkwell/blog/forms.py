# blog/forms.py
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "category", "tags", "content", "published"]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
            "content": forms.Textarea(attrs={"rows": 10}),
        }
