"""Database models for the project."""

from collections import defaultdict
from datetime import date
from functools import cached_property
from typing import Tuple, Type

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from df_site.models import AbstractPreferences
from paint_manager.compare import delta_e, rgb2lab, srgb
from paint_manager.utils import prepare_sorting_string, preserve_request_query


class Brand(models.Model):
    """A brand of model paint."""

    name = models.CharField(max_length=200, db_index=True, verbose_name=_("nom"))
    logo = models.ImageField(verbose_name=_("logo"), default=None, null=True)

    class Meta:
        """Return the options of this model."""

        verbose_name = _("marque")
        verbose_name_plural = _("marques")

    def __str__(self):
        """Return the name of the paint."""
        return self.name


class Paint(models.Model):
    """A model paint."""

    FINISHES = [
        ("matt", _("mat")),
        ("fluo", _("fluorescent")),
        ("gloss", _("brillant")),
        ("transparent", _("transparent")),
        ("metallic", _("métallique")),
        ("satin", _("satiné")),
        ("varnish", _("vernis")),
        ("iridescent", _("irisé")),
    ]
    SOLVENTS = [
        ("pigments", _("pigments")),
        ("acrylic", _("acrylique")),
        ("enamel", _("enamel")),
        ("lacquer", _("laque")),
    ]
    PACKAGINGS = [
        ("bottle", _("pot")),
        ("spray", _("bombe")),
        ("eye dropper", _("compte-goutte")),
    ]
    name = models.CharField(max_length=200, db_index=True, verbose_name=_("nom"))
    sort_name = models.CharField(  # noqa DJ001
        max_length=200, db_index=True, verbose_name=_("nom pour le tri"), default="", blank=True
    )
    reference = models.CharField(max_length=200, db_index=True, verbose_name=_("référence"))
    sort_reference = models.CharField(  # noqa DJ001
        max_length=200, db_index=True, verbose_name=_("référence"), default="", blank=True
    )
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE, verbose_name=_("marque"))
    finish = models.CharField(  # noqa DJ001
        max_length=12,
        db_index=True,
        choices=FINISHES,
        default=FINISHES[0][0],
        blank=True,
        null=True,
        verbose_name=_("finition"),
    )
    solvent = models.CharField(
        max_length=12,
        db_index=True,
        choices=SOLVENTS,
        default=SOLVENTS[0][0],
        verbose_name=_("type"),
    )
    packaging = models.CharField(  # noqa DJ001
        max_length=12,
        db_index=True,
        choices=PACKAGINGS,
        default=PACKAGINGS[0][0],
        blank=True,
        null=True,
        verbose_name=_("format"),
    )  # noqa DJ001
    size = models.CharField(max_length=20, db_index=True, blank=True, null=True, verbose_name=_("taille"))  # noqa DJ001
    color_r = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(255)],
        db_index=True,
        verbose_name=_("composante R"),
    )
    color_g = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(255)],
        db_index=True,
        verbose_name=_("composante V"),
    )
    color_b = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(255)],
        db_index=True,
        verbose_name=_("composante B"),
    )

    class Meta:
        """Meta options for this model."""

        verbose_name = _("peinture")
        verbose_name_plural = _("peintures")
        ordering = ("sort_reference", "size")

    def __str__(self):
        """Return the paint as a string."""
        if self.name and self.reference:
            return (
                f"{self.reference} {self.name} "
                f"({self.get_packaging_display()} {self.size}, "
                f"{self.get_solvent_display()}, "
                f"{self.get_finish_display()})"
            )
        return self.name or self.reference

    __str__.admin_order_field = "sort_name"

    def get_absolute_url(self):
        """Return the URL of the paint."""
        return reverse("paint_detail", kwargs={"pk": self.id})

    def html_color(self, height=1):
        """Return the color as a HTML small square."""
        """Display the color as a small square."""
        msg = (
            "<span "
            f'class="d-inline-block html-color-{height}" '
            f'data-mpm-color="#{self.color_r:02x}{self.color_g:02x}{self.color_b:02x}"'
            "></span>"
        )
        return mark_safe(msg)  # noqa S308

    html_color.short_description = _("Aperçu")

    def html_color_large(self):
        """Return the color as a HTML square."""
        return self.html_color(height=5)

    html_color_large.short_description = _("Aperçu")

    @cached_property
    def lab(self) -> Tuple[float, float, float]:
        """Return the color in the LAB space."""
        return rgb2lab(self.color)

    @property
    def color(self) -> Tuple[int, int, int]:
        """Return the color as a RGB tuple."""
        return self.color_r, self.color_g, self.color_b

    def similar_paints(self, request: HttpRequest, user=None):
        """Return the list of similar paints."""
        solvent = None
        brands = []
        if user and user.is_authenticated:
            solvent = user.solvent
            brands = list(user.preferred_brands.all())
        if len(brands) == 0:
            brands = list(Brand.objects.all())
        print(brands)

        bound = 50
        references = defaultdict(lambda: set())
        qs = RegisteredSimilarPaint.objects.filter(Q(paint_a=self) | Q(paint_b=self))
        for rsp in qs.select_related("source"):
            if rsp.paint_a == self:
                references[rsp.paint_b.id].add((rsp.source.name, rsp.source.url))
            else:
                references[rsp.paint_a.id].add((rsp.source.name, rsp.source.url))
        qs = Paint.objects.filter(
            Q(
                color_r__gte=self.color_r - bound,
                color_r__lte=self.color_r + bound,
                color_g__gte=self.color_g - bound,
                color_g__lte=self.color_g + bound,
                color_b__gte=self.color_b - bound,
                color_b__lte=self.color_b + bound,
            )
            | Q(id__in=references),
            brand__in=brands,
        )
        qs = qs.select_related("brand")
        if solvent:
            qs = qs.filter(solvent=solvent)
        propositions = list(qs)
        similair_paints = [SimilarPaint(x, self, references=references[x.id]) for x in propositions]
        similair_paints.sort(key=lambda x: x.difference)
        by_key = {x.paint.id: x for x in similair_paints}
        for user_paint in UserPaint.objects.filter(paint__in=propositions, user=user):
            by_key[user_paint.paint_id].user_paints.append(user_paint)
        preserved_filters = request.GET.get("_changelist_filters")
        if preserved_filters:
            preserved_filters = urlencode({"_changelist_filters": preserved_filters})
            url_suffix = f"?{preserved_filters}"
        else:
            url_suffix = ""
        ctx = {"similar_paints": similair_paints, "url_suffix": url_suffix}
        msg = render_to_string("paint_manager/similar_paints.html", context=ctx)
        return mark_safe(msg)  # noqa S308

    def color_difference(self, other_paint: "Paint"):
        """Return the difference between the two paint."""
        return delta_e(self.lab, other_paint.lab)

    def stock_level(self, request, user):
        """Return the current level of all paints."""
        values = list(UserPaint.objects.filter(paint=self, user=user))
        add_url = reverse("paint_add", kwargs={"pk": self.pk})
        add_url = preserve_request_query(request, add_url)
        ctx = {"stock_level": values, "paint": self, "add_url": add_url}
        msg = render_to_string("paint_manager/user_paint_stock.html", context=ctx)
        return mark_safe(msg)  # noqa S308

    # noinspection PyUnusedLocal
    @staticmethod
    def update_sort_name(sender: Type["Paint"], instance: "Paint", **kwargs):
        """Signal called before each paint save, to update the sorting name."""
        instance.sort_name = prepare_sorting_string(instance.name)
        instance.sort_reference = prepare_sorting_string(instance.reference)

    def display_name(self):
        """Display the name field, and order by the sort_name field."""
        return self.name

    display_name.short_description = _("nom")
    display_name.admin_order_field = "sort_name"

    def display_reference(self):
        """Display the reference field, and order by the sort_reference field."""
        return self.reference

    display_reference.short_description = _("nom")
    display_reference.admin_order_field = "sort_reference"

    def html_usage(self):
        """Display the current remaining quantity."""
        msg = ""
        if hasattr(self, "remaining") and self.remaining is not None:
            s = int(self.remaining / 10.0)
            r = "▮" * s + "▯" * (10 - s)
            c = "danger"
            if s >= 7:
                c = "success"
            elif s >= 3:
                c = "warning"
            msg += f'<span class="text-{c}">{r}</span>'
        return mark_safe(msg)  # noqa S308

    html_usage.short_description = _("Stock")
    html_usage.admin_order_field = "remaining"


class Reference(models.Model):
    """Reference website for paint equivalences."""

    name = models.CharField(verbose_name=_("nom"), max_length=100, db_index=True, default="-")
    url = models.URLField(
        verbose_name=_("lien"),
        max_length=255,
        db_index=True,
        default="http://example.com/",
    )

    class Meta:
        """Meta options for the model."""

        verbose_name = _("référence")
        verbose_name_plural = _("références")

    def __str__(self):
        """Return the name."""
        return self.name


class RegisteredSimilarPaint(models.Model):
    """Two similar paints, as presented in a reference."""

    source = models.ForeignKey(Reference, on_delete=models.CASCADE)
    paint_a = models.ForeignKey(Paint, on_delete=models.CASCADE, related_name="similar_a")
    paint_b = models.ForeignKey(Paint, on_delete=models.CASCADE, related_name="similar_b")

    class Meta:
        """Meta options for the model."""

        verbose_name = _("peintures similaires")
        verbose_name_plural = _("peintures similaires")

    def __str__(self):
        """Return the two similar paints."""
        return f"{self.paint_a} ~ {self.paint_b}"


class SimilarPaint:
    """A paint similar to another one."""

    def __init__(self, proposition: Paint, original: Paint, references=None):
        """Initialize this comparison, linked to a reference source."""
        self.paint = proposition
        self.original = original
        self.difference = original.color_difference(proposition)
        self.user_paints = []
        self.references = references

    def srgb_difference(self):
        """Display the delta between the two colors."""
        return srgb(self.original.color, self.paint.color)


class UserPaint(models.Model):
    """A bottle of paint owned by a user."""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("utilisateur"),
    )
    paint = models.ForeignKey(to=Paint, on_delete=models.CASCADE, verbose_name=_("peinture"))
    remaining = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        db_index=True,
        verbose_name=_("niveau restant"),
        default=100,
        blank=True,
    )
    comment = models.TextField(blank=True, default="", verbose_name=_("commentaire"))
    buying_date = models.DateField(
        blank=True,
        db_index=True,
        null=True,
        verbose_name=_("date d'achat"),
        default=date.today,
    )

    class Meta:
        """Meta options for the model."""

        verbose_name = _("peinture en stock")
        verbose_name_plural = _("peintures en stock")
        ordering = ("paint__sort_name",)

    def __str__(self):
        """Return the string representation of the paint."""
        return str(self.paint)

    def html_color(self):
        """Display the color as a small square."""
        return self.paint.html_color(1)

    html_color.short_description = _("Aperçu")
    html_color.admin_order_field = (
        "paint__color_r",
        "paint__color_g",
        "paint__color_b)",
    )

    def html_usage(self):
        """Display the current remaining quantity."""
        s = int(self.remaining / 10.0)
        r = "▮" * s + "▯" * (10 - s)
        c = "danger"
        if s >= 7:
            c = "success"
        elif s >= 3:
            c = "warning"
        msg = f'<span class="text-{c}">{r}</span>'
        return mark_safe(msg)  # noqa S308

    html_usage.short_description = _("Niveau")
    html_usage.admin_order_field = "remaining"

    def name(self):
        """Return the name but order by the reference."""
        return str(self)

    name.short_description = _("Référence")
    name.admin_order_field = "paint__reference"


class PaintOwner(AbstractUser, AbstractPreferences):
    """A user of the paint manager, that owns several paints."""

    preferred_brands = models.ManyToManyField(to=Brand, blank=True, verbose_name=_("marques préférées"))
    solvent = models.CharField(  # noqa DJ001
        max_length=12,
        db_index=True,
        choices=Paint.SOLVENTS,
        null=True,
        verbose_name=_("type préféré"),
    )

    class Meta:
        """Meta options for the model."""

        verbose_name = _("user")
        verbose_name_plural = _("users")
