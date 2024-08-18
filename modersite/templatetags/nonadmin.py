"""Custom template tags for rendering components in templates."""

from typing import Optional

from django.contrib.admin.views.main import PAGE_VAR
from django.template.library import Library
from django.utils.safestring import mark_safe

from modersite.components.list import Component

register = Library()


@register.simple_tag(takes_context=True)
def component(context, comp: Component):
    """Render a HTML component in a template."""
    text = comp.render(context)
    return mark_safe(text)  # noqa S308


@register.simple_tag
def component_list_url(cl, page: Optional[int] = None):
    """Generate an individual page index link in a paginated list."""
    kwargs = {}
    if page is not None:
        kwargs[PAGE_VAR] = page
    return cl.get_query_string(kwargs)
