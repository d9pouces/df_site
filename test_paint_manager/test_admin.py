"""Test all admin views."""

from typing import Dict

from django.core.exceptions import PermissionDenied

from df_site.testing.multiple_views import TestModel
from paint_manager.models import PaintOwner


class TestPaintOwnerAdmin(TestModel):
    """Test the PaintOwner admin."""

    expected_responses = {
        "auth_user_password_change": {
            None: 302,
            "staff": PermissionDenied,
            "admin": 200,
        },
    } | TestModel.expected_responses

    def get_object(self):
        """Return an object to test."""
        return PaintOwner(username="Test user")

    def get_common_kwargs_for_object(self, obj) -> Dict[str, str]:
        """Return the common kwargs for all views of the provided object."""
        return {"object_id": str(obj.pk), "id": str(obj.pk)}
