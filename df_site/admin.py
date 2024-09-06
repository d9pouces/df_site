"""Admin classes for the df_site app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from df_site.models import AlertRibbon, PreferencesUser


@admin.register(AlertRibbon)
class AlertRibbonAdmin(admin.ModelAdmin):
    """Admin class for the alert ribbon model."""

    list_display = ("message", "color", "start_date", "end_date", "is_active")
    list_filter = ("color", "start_date", "end_date", "is_active", "position")
    search_fields = ("summary",)
    fields = ["summary", "url", "message", "color", "start_date", "end_date", "is_active", "position"]


@admin.register(PreferencesUser)
class PreferencesUserAdmin(UserAdmin):
    """Admin class for the preferences user model."""

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "color_theme", "display_online", "email_notifications")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
