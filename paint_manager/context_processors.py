"""Add the user preferences to have a customized search bar."""

from typing import Any, Dict

from django.http import HttpRequest

from df_site.components.list import ModelListComponent
from paint_manager.models import PaintOwner


def search_infos(request: HttpRequest) -> Dict[str, Any]:
    """Adds a few values to the request context."""
    kwargs = {}
    # noinspection PyTypeChecker
    user: PaintOwner = request.user
    if user.is_authenticated:
        if user.solvent:
            kwargs["solvent__exact"] = user.solvent
        brand = user.preferred_brands.all().first()
        if brand:
            kwargs["brand__id__exact"] = brand.pk
    return {"SEARCH_KWARGS": kwargs, "SEARCH_VAR": ModelListComponent.search_var}
