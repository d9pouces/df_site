"""Admin classes for the df_site app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from paint_manager.models import Brand, PaintOwner


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin class for the brand model."""

    list_display = ("name",)
    search_fields = ("name",)
    fields = [
        "name",
    ]


@admin.register(PaintOwner)
class PaintOwnerAdmin(UserAdmin):
    """Admin class for the paint owner model."""

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "color_theme",
                    "display_online",
                    "email_notifications",
                    "preferred_brands",
                    "solvent",
                )
            },
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
    autocomplete_fields = ["preferred_brands"]
