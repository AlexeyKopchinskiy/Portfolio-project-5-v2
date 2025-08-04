from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    newsletter_opt_in = models.BooleanField(default=False)
    has_paid_author = models.BooleanField(default=False)
    has_paid_reviewer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
