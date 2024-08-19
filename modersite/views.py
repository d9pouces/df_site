"""Views for the modersite app."""

import json
import logging

from df_websockets.tasks import set_websocket_topics
from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from modersite.components.list import ModelListComponent
from modersite.components.list_filters import BooleanFieldListFilter, ChoicesFieldListFilter, DateFieldListFilter
from modersite.models import AlertRibbon

logger = logging.getLogger(__name__)


def site_webmanifest_view(request: HttpRequest) -> HttpResponse:
    """Generate a site.webmanifest view."""
    result = {
        "name": settings.DF_SITE_TITLE,
        "short_name": settings.DF_SITE_TITLE,
        "icons": [
            {"src": static("favicon/android-chrome-1192x192.png"), "sizes": "192x192", "type": "image/png"},
            {"src": static("favicon/android-chrome-512x512.png"), "sizes": "512x512", "type": "image/png"},
        ],
        "theme_color": settings.DF_ANDROID_THEME_COLOR,
        "background_color": settings.DF_ANDROID_BACKGROUND_COLOR,
        "display": "standalone",
    }

    return JsonResponse(result)


@csrf_exempt
def csp_report_view(request: HttpRequest) -> HttpResponse:
    """View to receive CSP reports, displaying them to the user in DEBUG mode."""
    logger.info("CSP report: %s", request.body)
    if settings.DEBUG:
        try:
            content = json.loads(request.body)
            csp_report = content["csp-report"]
            msg = (
                f"<strong>CSP violation</strong> on this <a href='{csp_report['document-uri']}'>page</a>:"
                f" {csp_report['effective-directive']} forbids the use of"
                f" '{csp_report['blocked-uri']}' URIs."
            )
            messages.error(request, mark_safe(msg))  # noqa
        except ValueError:
            pass
    return HttpResponse(status=204)


class BrowserConfigView(TemplateView):
    """View for the browserconfig.xml file."""

    template_name = "favicon/browserconfig.xml"
    content_type = "application/xml"


class IndexView(TemplateView):
    """Default index view."""

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["ribbon_list"] = ModelListComponent(
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
        set_websocket_topics(self.request)
        return context


class DemoView(TemplateView):
    """Demo view with many Bootstrap functionnalities."""

    template_name = "demo.html"

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        set_websocket_topics(self.request)
        messages.error(self.request, "This is an error message.")
        return context


class PopupDemoView(TemplateView):
    """Popup view with many Bootstrap functionnalities."""

    template_name = "popup_demo.html"
