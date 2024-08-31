"""Groups all views related to the users."""

from typing import Optional
from urllib.parse import parse_qsl

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, FormView, TemplateView, UpdateView

from df_site.components.detail import ModelDetailView
from df_site.users.views import UserSettingsView
from paint_manager.forms import AddUserPaintForm, UserSettingsForm
from paint_manager.lists import paints_list
from paint_manager.models import Paint, UserPaint


class CustomUserSettingsView(UserSettingsView):
    """View for the user settings page."""

    form_class = UserSettingsForm


class PaintDetailUrls:
    """Mixin to add URLs to the context of a paint detail view."""

    def update_context(self, context, paint: Paint):
        """Update the context with the URLs for the paint detail page."""
        index_url = reverse("index")
        # noinspection PyUnresolvedReferences
        preserved_filters = self.request.GET.get("_changelist_filters")
        preserved_query = ""
        cancel_url = paint.get_absolute_url()
        if preserved_filters:
            parsed_filters = parse_qsl(preserved_filters)
            preserved_query += urlencode({"_changelist_filters": preserved_filters})
            index_url += "?" + urlencode(parsed_filters)
            cancel_url += "?" + preserved_query
        context["INDEX_URL"] = index_url
        context["CANCEL_URL"] = cancel_url
        context["ACTION_URL"] = "?" + preserved_query


class PaintDetailView(PaintDetailUrls, ModelDetailView):
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
        self.update_context(context, self.object)
        if self.request.user.is_authenticated:
            context["similar_paints"] = self.object.similar_paints(self.request, self.request.user)
            context["stock_level"] = self.object.stock_level(self.request, self.request.user)
        return context


class UserPaintUpdateView(PaintDetailUrls, UpdateView):
    """View for updating a user paint."""

    model = UserPaint
    form_class = AddUserPaintForm

    def get_object(self, queryset=None):
        """Return the object the view is displaying."""
        return get_object_or_404(UserPaint, pk=self.kwargs["pk"], user=self.request.user)

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        self.update_context(context, self.object.paint)
        context["PAGE_TITLE"] = _("Modifier une peinture au stock")
        return context

    def get_success_url(self):
        """Return the URL to redirect to after a successful form submission."""
        preserved_filters = self.request.GET.get("_changelist_filters")
        success_url = self.object.paint.get_absolute_url()
        url_suffix = ""
        if preserved_filters:
            url_suffix += "?" + urlencode({"_changelist_filters": preserved_filters})
        return success_url + url_suffix


class UserPaintDeleteView(PaintDetailUrls, DeleteView):
    """View for deleting a user paint."""

    model = UserPaint

    def get_object(self, queryset=None):
        """Return the object the view is displaying."""
        return get_object_or_404(UserPaint, pk=self.kwargs["pk"], user=self.request.user)

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        self.update_context(context, self.object.paint)
        context["PAGE_TITLE"] = _("Supprimer une peinture du stock")
        return context

    def get_success_url(self):
        """Return the URL to redirect to after a successful form submission."""
        preserved_filters = self.request.GET.get("_changelist_filters")
        url_suffix = ""
        success_url = self.object.paint.get_absolute_url()
        if preserved_filters:
            url_suffix += "?" + urlencode({"_changelist_filters": preserved_filters})
        return success_url + url_suffix


class PaintAddView(PaintDetailUrls, FormView):
    """View for adding a paint."""

    template_name = "paint_manager/add_paint.html"
    form_class = AddUserPaintForm

    def get_context_data(self, **kwargs):
        """Get the context data for the view."""
        context = super().get_context_data(**kwargs)
        paint = get_object_or_404(Paint, pk=self.kwargs["pk"])
        context["paint"] = paint
        self.update_context(context, paint)
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
