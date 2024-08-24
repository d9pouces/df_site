"""Groups all views related to the users."""

from django.views.generic import TemplateView

from df_site.users.views import UserSettingsView
from paint_manager.forms import UserSettingsForm
from paint_manager.lists import paints_list


class CustomUserSettingsView(UserSettingsView):
    """View for the user settings page."""

    form_class = UserSettingsForm


class IndexView(TemplateView):
    """Default index view."""

    template_name = "paint_manager/index.html"

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["paints_list"] = paints_list
        return context
