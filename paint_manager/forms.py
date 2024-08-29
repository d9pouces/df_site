"""Forms for the paint_manager app."""

from django import forms
from django.contrib.auth import get_user_model

from paint_manager.models import UserPaint


class UserSettingsForm(forms.ModelForm):
    """Form for the user settings page."""

    class Meta:
        """Meta options for the form."""

        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "color_theme",
            "email_notifications",
            "display_online",
            "preferred_brands",
            "solvent",
        ]


class AddUserPaintForm(forms.ModelForm):
    """Form for adding a user paint."""

    class Meta:
        """Meta options for the form."""

        model = UserPaint
        fields = ["remaining", "comment", "buying_date"]
