"""Groups all views related to the users."""

from django.views.generic import TemplateView

from df_site.components.detail import ModelDetailView
from df_site.users.views import UserSettingsView
from paint_manager.forms import UserSettingsForm
from paint_manager.lists import paints_list
from paint_manager.models import Paint


class CustomUserSettingsView(UserSettingsView):
    """View for the user settings page."""

    form_class = UserSettingsForm


class PaintDetailView(ModelDetailView):
    """View for a paint detail page."""

    model = Paint
    fields = (
        "html_color_large",
        ("name", "reference"),
        ("finish", "solvent"),
        ("packaging", "size", "stock_level"),
        "similar_paints",
    )


class IndexView(TemplateView):
    """Default index view."""

    template_name = "paint_manager/index.html"

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["paints_list"] = paints_list
        return context
