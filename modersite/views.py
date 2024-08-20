"""Views for the modersite app."""

import json
import logging

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

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
