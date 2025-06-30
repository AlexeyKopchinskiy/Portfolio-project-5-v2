from django.contrib import admin
from .models import Page


# Register your models here.


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "updated")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "content")
