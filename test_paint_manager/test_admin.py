"""Test all admin views."""

from paint_manager.models import PaintOwner
from tests_df_site.test_admin import TestPreferencesUserAdmin


class TestPaintOwnerAdmin(TestPreferencesUserAdmin):
    """Test the PaintOwner admin."""

    model = PaintOwner
