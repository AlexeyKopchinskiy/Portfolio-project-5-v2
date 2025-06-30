from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(
        upload_to="blog_images/", blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
