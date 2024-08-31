"""Custom filters for the paint_manager app."""

from django.contrib.admin.utils import get_last_value_from_parameters
from django.db.models import Count, Q
from django.utils.translation import gettext as _

from df_site.components.list_filters import (
    FieldListFilter,
)


class IsOwnedFieldListFilter(FieldListFilter):
    """Filter paints that are currently owned (or not)."""

    def __init__(self, field, request, params, model, model_admin, field_path="reference"):
        """Initialize the filter."""
        self.lookup_kwarg = field_path
        self.lookup_val = get_last_value_from_parameters(params, self.lookup_kwarg)
        super().__init__(field, request, params, model, model_admin, field_path)
        if self.used_parameters and self.lookup_kwarg in self.used_parameters and self.lookup_val in ("1", "0"):
            self.lookup_val = bool(int(self.lookup_val))
        self.title = _("En stock")

    def expected_parameters(self):
        """Return the expected parameters."""
        return [self.lookup_kwarg]

    def queryset(self, request, queryset):
        """Return the filtered queryset."""
        value = self.lookup_val
        if value is True:
            queryset = queryset.filter(user_count__gt=0)
        elif value is False:
            queryset = queryset.filter(user_count=0)
        return queryset

    def get_facet_counts(self, pk_attname, filtered_qs):
        """Return the facet counts."""
        return {
            "true__c": Count("pk", filter=Q(user_count__gt=0)),
            "false__c": Count("pk", filter=Q(user_count=0)),
        }

    def choices(self, changelist):
        """Return a list of choices."""
        field_choices = dict(self.field.flatchoices)
        add_facets = changelist.add_facets
        facet_counts = self.get_facet_queryset(changelist) if add_facets else None
        # noinspection PyTypeChecker
        for lookup, title, count_field, value in (
            (None, _("All"), None, None),
            ("1", field_choices.get(True, _("Yes")), "true__c", True),
            ("0", field_choices.get(False, _("No")), "false__c", False),
        ):
            if add_facets:
                if count_field is not None:
                    count = facet_counts[count_field]
                    title = f"{title} ({count})"
            yield {
                "selected": self.lookup_val is value,
                "query_string": changelist.get_query_string(
                    {self.lookup_kwarg: lookup},
                ),
                "display": title,
            }
