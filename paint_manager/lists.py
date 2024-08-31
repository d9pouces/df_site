"""List components."""

from django.db import models
from django.db.models import Count, Max, Q
from django.http import HttpRequest
from django.utils.translation import gettext as _

from df_site.components.list import ModelListComponent
from df_site.components.list_filters import (
    AllValuesFieldListFilter,
    ChoicesFieldListFilter,
    RelatedFieldListFilter,
)
from paint_manager.filters import IsOwnedFieldListFilter
from paint_manager.models import Paint


class PaintListComponent(ModelListComponent):
    """List component for the paints."""

    list_display_anonymous = [
        "display_name",
        "display_reference",
        "html_color",
        "brand",
        "finish",
        "solvent",
        "packaging",
        "size",
    ]
    list_display_authenticated = [
        "display_name",
        "display_reference",
        "html_usage",
        "html_color",
        "brand",
        "finish",
        "solvent",
        "packaging",
        "size",
    ]

    def __init__(self):
        """Initialize the list component."""
        super().__init__(
            model=Paint,
            list_per_page=30,
            search_fields=["name", "reference"],
            list_display=[],
            list_select_related=["brand"],
            sortable_by=[
                "display_name",
                "display_reference",
                "brand",
                "finish",
                "solvent",
                "packaging",
                "size",
                "html_usage",
            ],
            list_filter=[
                ("reference", IsOwnedFieldListFilter),
                ("brand", RelatedFieldListFilter),
                ("finish", ChoicesFieldListFilter),
                ("solvent", ChoicesFieldListFilter),
                ("packaging", ChoicesFieldListFilter),
                ("size", AllValuesFieldListFilter),
            ],
            search_help_text=None,
            filters_on_right=True,
            filters_title=_("Filters"),
        )

    def get_list_filter(self, request, **kwargs):
        """Return the list of available filters."""
        return self.list_filter

    def get_queryset(self, request: HttpRequest, **kwargs) -> models.QuerySet:
        """Return the queryset based on the user's authentication status."""
        qs = super().get_queryset(request, **kwargs)
        if request.user.is_authenticated:
            qs = qs.annotate(remaining=Max("userpaint__remaining", filter=Q(userpaint__user=request.user)))
            qs = qs.annotate(user_count=Count("userpaint", filter=Q(userpaint__user=request.user)))
        return qs

    def get_list_display(self, request: HttpRequest, **kwargs):
        """Return the list display based on the user's authentication status."""
        if request.user.is_authenticated:
            return self.list_display_authenticated
        return self.list_display_anonymous


paints_list = PaintListComponent()
