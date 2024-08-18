"""Components for displaying a list of items in a table."""

from typing import Callable, List, Optional, Tuple, Type, Union

from django.contrib.admin import ListFilter, ShowFacets, SimpleListFilter, widgets
from django.contrib.admin.options import IS_FACETS_VAR, IS_POPUP_VAR
from django.contrib.admin.templatetags.admin_list import date_hierarchy, result_headers, results
from django.contrib.admin.utils import get_fields_from_path, lookup_spawns_duplicates
from django.contrib.admin.views.main import ALL_VAR, ORDER_VAR, PAGE_VAR, SEARCH_VAR, ChangeList
from django.core.exceptions import FieldDoesNotExist
from django.core.paginator import Paginator
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.db.models.functions.text import Substr, Upper
from django.http import HttpRequest
from django.utils.http import urlencode
from django.utils.text import smart_split, unescape_string_literal
from django.utils.translation import gettext as _

from modersite.components.base import Component


class ModelListChangeList(ChangeList):
    """Customized ChangeList for ModelListComponent."""

    formset = None
    paginator: Paginator

    def url_for_result(self, result: models.Model):
        """Return the URL for a result, trying to use the get_absolute_url method."""
        if hasattr(result, "get_absolute_url"):
            return result.get_absolute_url()
        return f"/{self.opts.app_label}/{self.opts.model_name}/{result.pk}/show/"


class ModelListComponent(Component):
    """A component that can display a list as table, with filters and a search bar."""

    template: str = "components/list.html"
    page_var = PAGE_VAR
    all_var = ALL_VAR
    order_var = ORDER_VAR
    search_var = SEARCH_VAR
    list_editable: List[str] = []
    pagination_on_top = True
    pagination_on_bottom = True

    def __init__(
        self,
        model: Type[models.Model],
        template: str = "modersite/components/list.html",
        list_select_related: Optional[List[str]] = None,
        list_display: List[str] = None,
        list_display_links: List[str] = None,
        list_filter: List[Union[str, Tuple[str, Type[ListFilter]], Callable]] = None,
        date_hierarchy: Optional[str] = None,
        search_fields: List[str] = None,
        list_per_page: int = 20,
        list_max_show_all: int = 200,
        sortable_by: List[str] = None,
        search_help_text: str = "",
        show_facets: ShowFacets = ShowFacets.ALLOW,
        show_full_result_count: bool = True,
        ordering: List[str] = None,
    ):
        """Create a new list component."""
        super().__init__()
        self.model: Type[models.Model] = model
        self.opts = model._meta
        self.template: str = template
        self.list_select_related: Optional[List[str]] = list_select_related
        self.list_display: List[str] = list_display or ["__str__"]
        self.list_display_links: List[str] = list_display_links or []
        self.list_filter: List[Union[str, Tuple[str, Type[ListFilter], Callable]]] = list_filter or []
        self.date_hierarchy: Optional[str] = date_hierarchy
        self.search_fields: List[str] = search_fields or []
        self.list_per_page: int = list_per_page
        self.list_max_show_all: int = list_max_show_all
        self.sortable_by: List[str] = sortable_by or []
        self.search_help_text: str = search_help_text
        self.show_facets: ShowFacets = show_facets
        self.show_full_result_count: bool = show_full_result_count
        self.ordering: List[str] = ordering or []

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def get_change_list_class(self, request: HttpRequest) -> Type[ChangeList]:
        """Return the ChangeList class to use for this component."""
        return ModelListChangeList

    def get_change_list(self, request: HttpRequest) -> ChangeList:
        """Return the ChangeList instance to use for this component."""
        cls = self.get_change_list_class(request)
        return cls(
            request,
            self.model,
            self.list_display,
            self.list_display_links,
            self.list_filter,
            self.date_hierarchy,
            self.search_fields,
            self.list_select_related,
            self.list_per_page,
            self.list_max_show_all,
            self.list_editable,
            self,
            self.sortable_by,
            self.search_help_text,
        )

    # noinspection PyUnusedLocal
    def get_queryset(self, request: HttpRequest) -> models.QuerySet:
        """Return the queryset to use for this component."""
        qs = self.model.objects.all()
        if self.list_select_related:
            qs = qs.select_related(*self.list_select_related)
        return qs

    # noinspection PyMethodMayBeStatic
    def get_preserved_filters(self, request: HttpRequest):
        """Return the preserved filters querystring."""
        preserved_filters = request.GET.urlencode()
        if preserved_filters:
            return urlencode({"_changelist_filters": preserved_filters})
        return ""

    # noinspection PyUnusedLocal
    def to_field_allowed(self, request, to_field):
        """Mimic the behavior of the ModelAdmin."""
        try:
            field = self.opts.get_field(to_field)
        except FieldDoesNotExist:
            return False

        return field.primary_key

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def has_change_permission(self, request: HttpRequest, obj=None):
        """Mimic the behavior of the ModelAdmin."""
        return False

    def lookup_allowed(self, lookup, value, request=None):
        """Mimic the behavior of the ModelAdmin."""
        model = self.model
        # Check FKey lookups that are allowed, so that popups produced by
        # ForeignKeyRawIdWidget, on the basis of ForeignKey.limit_choices_to,
        # are allowed to work.
        for fk_lookup in model._meta.related_fkey_lookups:
            # As ``limit_choices_to`` can be a callable, invoke it here.
            if callable(fk_lookup):
                fk_lookup = fk_lookup()
            if (lookup, value) in widgets.url_params_from_lookup_dict(fk_lookup).items():
                return True

        relation_parts = []
        prev_field = None
        part = ""
        parts = lookup.split(LOOKUP_SEP)
        for part in parts:
            try:
                field = model._meta.get_field(part)
            except FieldDoesNotExist:
                # Lookups on nonexistent fields are ok, since they're ignored
                # later.
                break
            if not prev_field or (
                prev_field.is_relation
                and field not in model._meta.parents.values()
                and field is not model._meta.auto_field
                and (model._meta.auto_field is None or part not in getattr(prev_field, "to_fields", []))
                and (field.is_relation or not field.primary_key)
            ):
                relation_parts.append(part)
            if not getattr(field, "path_infos", None):
                # This is not a relational field, so further parts
                # must be transforms.
                break
            prev_field = field
            model = field.path_infos[-1].to_opts.model

        if len(relation_parts) <= 1:
            # Either a local field filter, or no fields at all.
            return True
        valid_lookups = {self.date_hierarchy}
        # RemovedInDjango60Warning: when the deprecation ends, replace with:
        # for filter_item in self.get_list_filter(request):
        list_filter = self.get_list_filter(request) if request is not None else self.list_filter
        for filter_item in list_filter:
            if isinstance(filter_item, type) and issubclass(filter_item, SimpleListFilter):
                valid_lookups.add(filter_item.parameter_name)
            elif isinstance(filter_item, (list, tuple)):
                valid_lookups.add(filter_item[0])
            else:
                valid_lookups.add(filter_item)

        # Is it a valid relational lookup?
        return not {
            LOOKUP_SEP.join(relation_parts),
            LOOKUP_SEP.join(relation_parts + [part]),
        }.isdisjoint(valid_lookups)

    # noinspection PyUnusedLocal
    def get_list_filter(self, request):
        """Return a sequence containing the fields to be displayed as filters."""
        return self.list_filter

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def get_paginator(self, request: HttpRequest, queryset, per_page, orphans=0, allow_empty_first_page=True):
        """Return the paginator to use for this component."""
        return Paginator(queryset, per_page, orphans, allow_empty_first_page)

    # noinspection PyUnusedLocal
    def get_ordering(self, request: HttpRequest):
        """Return the ordering to use for this component."""
        return self.ordering or ()

    # noinspection PyUnusedLocal
    def get_search_fields(self, request: HttpRequest):
        """Return a sequence containing the fields to be searched."""
        return self.search_fields

    def get_search_results(
        self, request: HttpRequest, queryset: models.QuerySet, search_term: str
    ) -> Tuple[models.QuerySet, bool]:
        """Return the search result.

        Return a tuple containing a queryset to implement the search
        and a boolean indicating if the results may contain duplicates.
        """

        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith("^"):
                removeprefix = field_name.removeprefix("^")
                return f"{removeprefix}__istartswith"
            elif field_name.startswith("="):
                removeprefix = field_name.removeprefix("=")
                return f"{removeprefix}__iexact"
            elif field_name.startswith("@"):
                removeprefix = field_name.removeprefix("@")
                return f"{removeprefix}__search"
            # Use field_name if it includes a lookup.
            opts = self.opts
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == "pk":
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, "path_infos"):
                        # Update opts to follow the relation.
                        opts = field.path_infos[-1].to_opts
            # Otherwise, use the field with icontains.
            return f"{field_name}__icontains"

        may_have_duplicates = False
        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            orm_lookups = [construct_search(str(search_field)) for search_field in search_fields]
            term_queries = []
            for bit in smart_split(search_term):
                if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
                    bit = unescape_string_literal(bit)
                or_queries = models.Q.create(
                    [(orm_lookup, bit) for orm_lookup in orm_lookups],
                    connector=models.Q.OR,
                )
                term_queries.append(or_queries)
            queryset = queryset.filter(models.Q.create(term_queries))
            may_have_duplicates |= any(lookup_spawns_duplicates(self.opts, search_spec) for search_spec in orm_lookups)
        return queryset, may_have_duplicates

    def update_render_context(self, context):
        """Update the context before rendering the component."""
        cl = self.get_change_list(context["request"])
        context.update({"cl": cl, "opts": self.opts})
        context.update(self.get_pagination_context(cl))
        context.update(self.get_search_context(cl))
        context.update(self.get_hierarchy_context(cl))

    # noinspection PyMethodMayBeStatic
    def get_empty_value_display(self):
        """Return the value to display for an empty field."""
        return "-"

    def get_pagination_context(self, cl: ChangeList):
        """Return the context for the pagination."""
        headers = list(result_headers(cl))
        num_sorted_fields = 0
        for h in headers:
            if h["sortable"] and h["sorted"]:
                num_sorted_fields += 1
        pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
        page_range = cl.paginator.get_elided_page_range(cl.page_num) if pagination_required else []
        need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
        return {
            "pagination_required": pagination_required,
            "show_all_url": need_show_all_link and cl.get_query_string({self.all_var: ""}),
            "page_range": list(page_range),
            "ALL_VAR": self.all_var,
            "1": 1,
            "results": list(results(cl)),
            "result_headers": headers,
            "num_sorted_fields": num_sorted_fields,
        }

    def get_search_context(self, cl: ChangeList):
        """Return the context for the search bar."""
        return {
            "show_result_count": cl.result_count != cl.full_result_count,
            "search_var": self.search_var,
            "is_popup_var": IS_POPUP_VAR,
            "is_facets_var": IS_FACETS_VAR,
        }

    # noinspection PyMethodMayBeStatic
    def get_hierarchy_context(self, cl: ChangeList):
        """Return the context for the hierarchy of results.

        Currently only works for date fields.
        """
        # noinspection PyTestUnpassedFixture
        field_name = cl.date_hierarchy
        if not field_name:
            return {"show_hierarchy": False}
        field = get_fields_from_path(cl.model, field_name)[-1]
        if isinstance(field, models.CharField) or isinstance(field, models.TextField):
            hierarchy_data = first_letter_hierarchy(cl)
        else:
            hierarchy_data = date_hierarchy(cl)
        if hierarchy_data is not None:
            return {
                "show_hierarchy": True,
                "hierarchy_back": hierarchy_data["back"],
                "hierarchy_choices": hierarchy_data["choices"],
                "hierarchy_title": field.verbose_name,
            }
        return {"show_hierarchy": False}


def first_letter_hierarchy(cl: ChangeList):
    """Fetch all initials of a CharField."""
    # noinspection PyTestUnpassedFixture
    qs = (
        cl.queryset.annotate(hierarchy_initial=Upper(Substr(cl.date_hierarchy, 1, 1)))
        .values_list("hierarchy_initial", flat=True)
        .distinct()
    )
    values = set(qs)
    if not values:
        return None
    # noinspection PyTestUnpassedFixture
    initial_field = f"{cl.date_hierarchy}__istartswith"
    initial_value = cl.params.get(initial_field)
    if initial_value:
        cl.get_query_string(remove=[initial_field])
        back = {"link": cl.get_query_string(remove=[initial_field]), "title": _("All")}
    else:
        back = None
    return {
        "show": True,
        "back": back,
        "choices": [
            {
                "title": initial,
                "link": cl.get_query_string({initial_field: initial}) if initial != initial_value else None,
            }
            for initial in sorted(values)
        ],
    }
