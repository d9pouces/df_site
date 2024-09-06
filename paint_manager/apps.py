"""Configuration for the paint manager app."""

from django.apps import AppConfig
from django.db.models.signals import post_migrate, pre_save
from django.utils.translation import gettext_lazy as _


class PaintManagerConfig(AppConfig):
    """Configuration for the paint manager app."""

    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Peintures")
    name = "paint_manager"

    def ready(self):
        """Import signals and connect them."""
        from django.conf import settings

        from paint_manager.initialization.load import database_initialization
        from paint_manager.models import Paint

        pre_save.connect(Paint.update_sort_name, sender=self)
        if not settings.TESTING:
            post_migrate.connect(database_initialization, sender=self)
