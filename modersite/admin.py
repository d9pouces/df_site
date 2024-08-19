"""Admin classes for the modersite app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from modersite.models import AlertRibbon, PreferencesUser


@admin.register(AlertRibbon)
class AlertRibbonAdmin(admin.ModelAdmin):
    """Admin class for the alert ribbon model."""

    list_display = ("message", "color", "start_date", "end_date", "is_active")
    list_filter = ("color", "start_date", "end_date", "is_active", "position")
    search_fields = ("summary",)
    fields = ["summary", "url", "message", "color", "start_date", "end_date", "is_active", "position"]


@admin.register(PreferencesUser)
class PreferencesUserAdmin(UserAdmin):
    """Admin class for the custom user model."""

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    ("is_active", "is_staff"),
                    "is_superuser",
                    ("email_notifications", "display_online"),
                    "color_theme",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
