from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DeveloperProfile


@admin.register(DeveloperProfile)
class DeveloperProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "github_username",
        "github_connected",
        "created_at",
    )

    search_fields = (
        "user__username",
        "github_username",
    )