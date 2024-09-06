"""Admin classes for the df_site app."""

from django.contrib import admin

from df_site.models import AlertRibbon


@admin.register(AlertRibbon)
class AlertRibbonAdmin(admin.ModelAdmin):
    """Admin class for the alert ribbon model."""

    list_display = ("message", "color", "start_date", "end_date", "is_active")
    list_filter = ("color", "start_date", "end_date", "is_active", "position")
    search_fields = ("summary",)
    fields = ["summary", "url", "message", "color", "start_date", "end_date", "is_active", "position"]
