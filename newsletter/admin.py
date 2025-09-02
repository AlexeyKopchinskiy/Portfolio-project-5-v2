from django.contrib import admin
from django.core.mail import send_mail
from .models import Newsletter, Subscriber
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.


@admin.register(Newsletter)
class NewsletterAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = ("subject", "created_at", "scheduled_send", "sent")
    list_filter = ("sent", "scheduled_send")
    search_fields = ("subject", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    actions = ["send_newsletter"]

    def send_newsletter(self, request, queryset):
        subscribers = Subscriber.objects.filter(active=True)
        for newsletter in queryset:
            if not newsletter.sent:
                for subscriber in subscribers:
                    send_mail(
                        subject=newsletter.subject,
                        message=newsletter.content,
                        from_email="alexey@example.com",
                        recipient_list=[subscriber.email],
                    )
                newsletter.sent = True
                newsletter.save()
        self.message_user(request, "Selected newsletters have been sent.")

    send_newsletter.short_description = (
        "Send selected newsletters to active subscribers"
    )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "subscribed_at", "active")
    list_filter = ("active",)
    search_fields = ("email", "name")
    ordering = ("-subscribed_at",)
