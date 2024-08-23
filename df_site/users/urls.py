"""List of URLs for the df_site app."""

from django.urls import path

from df_site.users.views import UserSettingsView, theme_switch

app_name = "users"
urlpatterns = [
    path("theme-switch", theme_switch, name="theme_switch"),
    path("settings", UserSettingsView.as_view(), name="settings"),
]
