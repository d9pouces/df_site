"""Test all admin views."""

from df_site.models import AlertRibbon
from df_site.testing.multiple_views import TestModel


class TestAlertRibbonAdmin(TestModel):
    """Test the AlertRibbon admin."""

    def get_object(self):
        """Return an object to test."""
        return AlertRibbon(summary="Test ribbon")
