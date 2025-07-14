from django.contrib import admin
from .models import Newsletter, Subscriber
from django_summernote.admin import SummernoteModelAdmin  # ← Add this import


# Register your models here.


@admin.register(Newsletter)
class NewsletterAdmin(SummernoteModelAdmin):  # ← Update base class here
    summernote_fields = ("content",)
    list_display = ("subject", "created_at", "scheduled_send", "sent")
    list_filter = ("sent", "scheduled_send")
    search_fields = ("subject", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "subscribed_at", "active")
    list_filter = ("active",)
    search_fields = ("email", "name")
    ordering = ("-subscribed_at",)
