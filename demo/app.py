"""Configuration for the demo app."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DemoApp(AppConfig):
    """Configuration for the demo app."""

    default_auto_field = "django.db.models.AutoField"
    name = "demo"
    verbose_name = _("Demo app")
