from django.db import models

# Create your models here.


class Newsletter(models.Model):
    """Model representing a newsletter issue."""

    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_send = models.DateTimeField(blank=True, null=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subject


class Subscriber(models.Model):
    """Model representing a newsletter subscriber."""

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
