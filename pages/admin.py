from django.contrib import admin
from .models import Page, ContactMessage


# Register your models here.


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "updated")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "content")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "timestamp")
    search_fields = ("name", "email", "subject", "message")
    ordering = ("-timestamp",)
