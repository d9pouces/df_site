"""Groups all views related to the users."""

from typing import Optional
from urllib.parse import parse_qsl

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.translation import gettext as _
from django.views.generic import FormView, TemplateView

from df_site.components.detail import ModelDetailView
from df_site.users.views import UserSettingsView
from paint_manager.forms import AddUserPaintForm, UserSettingsForm
from paint_manager.lists import paints_list
from paint_manager.models import Paint


class CustomUserSettingsView(UserSettingsView):
    """View for the user settings page."""

    form_class = UserSettingsForm


class PaintDetailView(ModelDetailView):
    """View for a paint detail page."""

    model = Paint
    fields = (
        "html_color_large",
        ("name", "reference"),
        ("finish", "solvent"),
        ("packaging", "size"),
    )

    def get_page_description(self) -> Optional[str]:
        """Return the page description."""
        return _("Caractéristiques de la peinture")

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        paint: Paint = self.object
        url = reverse("index")
        preserved_filters = self.request.GET.get("_changelist_filters")
        if preserved_filters:
            parsed_filters = parse_qsl(preserved_filters)
            url += "?" + urlencode(parsed_filters)
        context["INDEX_URL"] = url
        if self.request.user.is_authenticated:
            context["similar_paints"] = paint.similar_paints(self.request, self.request.user)
            context["stock_level"] = paint.stock_level(self.request, self.request.user)
        return context


class PaintAddView(FormView):
    """View for adding a paint."""

    template_name = "paint_manager/add_paint.html"
    form_class = AddUserPaintForm

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        paint = get_object_or_404(Paint, pk=self.kwargs["pk"])
        context["paint"] = paint
        preserved_filters = self.request.GET.get("_changelist_filters")
        preserved_query = ""
        index_url = reverse("index")
        cancel_url = paint.get_absolute_url()
        if preserved_filters:
            parsed_filters = parse_qsl(preserved_filters)
            index_url += "?" + urlencode(parsed_filters)
            preserved_query += urlencode({"_changelist_filters": preserved_filters})
            cancel_url += "?" + preserved_query
        context["ACTION_URL"] = "?" + preserved_query
        context["CANCEL_URL"] = cancel_url
        context["INDEX_URL"] = index_url
        context["PAGE_TITLE"] = _("Ajouter une peinture au stock")
        return context

    def form_valid(self, form):
        """Save the form and redirect to the paint detail page."""
        form.instance.user = self.request.user
        form.instance.paint = get_object_or_404(Paint, pk=self.kwargs["pk"])
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Return the URL to redirect to after a successful form submission."""
        preserved_filters = self.request.GET.get("_changelist_filters")
        url_suffix = ""
        success_url = reverse("paint_detail", kwargs={"pk": self.kwargs["pk"]})
        if preserved_filters:
            url_suffix += "?" + urlencode({"_changelist_filters": preserved_filters})
        return success_url + url_suffix


class IndexView(TemplateView):
    """Default index view."""

    template_name = "paint_manager/index.html"

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["paints_list"] = paints_list
        return context
