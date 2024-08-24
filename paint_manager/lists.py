"""List components."""

from django.utils.translation import gettext as _

from df_site.components.list import ModelListComponent
from df_site.components.list_filters import (
    AllValuesFieldListFilter,
    ChoicesFieldListFilter,
    RelatedFieldListFilter,
)
from paint_manager.models import Paint

paints_list = ModelListComponent(
    model=Paint,
    list_per_page=30,
    search_fields=["name", "reference"],
    list_display=["display_name", "display_reference", "brand", "finish", "solvent", "packaging", "size"],
    list_select_related=["brand"],
    sortable_by=["display_name", "display_reference", "brand", "finish", "solvent", "packaging", "size"],
    list_filter=[
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
