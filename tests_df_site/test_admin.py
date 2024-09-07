"""Test all admin views."""

from typing import Dict

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from df_site.models import AlertRibbon, PreferencesUser
from df_site.testing.multiple_views import TestModel


class TestAlertRibbonAdmin(TestModel):
    """Test the AlertRibbon admin."""

    def get_object(self):
        """Return an object to test."""
        return AlertRibbon(summary="Test ribbon")


class TestPreferencesUserAdmin(TestModel):
    """Test the PreferencesUser admin."""

    model = PreferencesUser

    expected_responses = {
        "auth_user_password_change": {
            None: 302,
            "staff": PermissionDenied,
            "admin": 200,
        },
    } | TestModel.expected_responses

    def test_model_admin(self):
        """Test the model admin."""
        if get_user_model() != self.model:
            self.skipTest(f"User model is not {self.model}")
        super().test_model_admin()

    def get_object(self):
        """Return an object to test."""
        return self.model(username="Test user")

    def get_common_kwargs_for_object(self, obj) -> Dict[str, str]:
        """Return the common kwargs for all views of the provided object."""
        return {"object_id": str(obj.pk), "id": str(obj.pk)}
