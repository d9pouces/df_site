"""Forms for the paint_manager app."""

from django import forms
from django.contrib.auth import get_user_model
from django.forms import NumberInput
from django.utils.translation import gettext as _

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


class RangeWidget(NumberInput):
    """Widget for a range input."""

    input_type = "range"


class AddUserPaintForm(forms.ModelForm):
    """Form for adding a user paint."""

    remaining = forms.IntegerField(
        min_value=0,
        max_value=100,
        label=_("niveau restant"),
        help_text=_("The amount of paint remaining in the pot."),
        widget=RangeWidget,
        initial=100,
    )

    class Meta:
        """Meta options for the form."""

        model = UserPaint
        fields = ["remaining", "comment", "buying_date"]
