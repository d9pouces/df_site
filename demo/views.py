"""Views for the demo app."""

import logging

from df_websockets.tasks import set_websocket_topics
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from modersite.components.detail import ModelDetailComponent, ModelDetailView
from modersite.components.list import ModelListComponent
from modersite.components.list_filters import BooleanFieldListFilter, ChoicesFieldListFilter, DateFieldListFilter
from modersite.models import AlertRibbon

logger = logging.getLogger(__name__)

ribbons_list = ModelListComponent(
    model=AlertRibbon,
    list_per_page=1,
    search_fields=["message"],
    list_display=["message", "position", "color", "url", "is_active"],
    sortable_by=["position", "color", "start_date", "end_date", "is_active"],
    list_filter=[
        ("position", ChoicesFieldListFilter),
        ("color", ChoicesFieldListFilter),
        ("is_active", BooleanFieldListFilter),
        ("start_date", DateFieldListFilter),
        ("end_date", DateFieldListFilter),
    ],
    search_help_text=None,
    date_hierarchy="message",
    filters_on_right=True,
    filters_title=_("Filters"),
)

ribbon_display = ModelDetailComponent(
    model=AlertRibbon,
)


class IndexView(TemplateView):
    """Default index view."""

    template_name = "demo/index.html"

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["ribbons_list"] = ribbons_list
        set_websocket_topics(self.request)
        return context


class RibbonDetailView(ModelDetailView):
    """Ribbon view."""

    model = AlertRibbon
    fieldsets = [
        (
            None,
            {
                "fields": [("summary", "url"), ("start_date", "end_date"), ("position", "color")],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["can-collapse"],
                "fields": ["message", "is_active"],
                "description": "These options are <a href='#'>for</a> advanced users only.",
            },
        ),
    ]


class DemoView(TemplateView):
    """Demo view with many Bootstrap functionnalities."""

    template_name = "demo/demo.html"

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        set_websocket_topics(self.request)
        messages.error(self.request, "This is an error message.")
        return context


class PopupDemoView(TemplateView):
    """Popup view with many Bootstrap functionnalities."""

    template_name = "demo/popup_demo.html"
