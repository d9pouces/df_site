"""Forms for the users app."""

from django import forms
from django.contrib.auth import get_user_model


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
        ]
