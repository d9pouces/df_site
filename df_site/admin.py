"""Admin classes for the df_site app."""

from functools import cached_property

try:
    from allauth.account.models import EmailAddress
except ImportError:
    EmailAddress = None
try:
    from allauth.mfa.models import Authenticator
except ImportError:
    Authenticator = None
try:
    from allauth.socialaccount.models import SocialAccount
except ImportError:
    SocialAccount = None
try:
    from allauth.usersessions.models import UserSession
except ImportError:
    UserSession = None
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from df_site.models import AlertRibbon, PreferencesUser


@admin.register(AlertRibbon)
class AlertRibbonAdmin(admin.ModelAdmin):
    """Admin class for the alert ribbon model."""

    list_display = ("message", "color", "start_date", "end_date", "is_active")
    list_filter = ("color", "start_date", "end_date", "is_active", "position")
    search_fields = ("summary",)
    fields = ["summary", "url", "message", "color", "start_date", "end_date", "is_active", "position"]


class EmailAddressInline(admin.TabularInline):
    """Inline for the email address model."""

    model = EmailAddress
    extra = 0


class SocialAccountInline(admin.TabularInline):
    """Inline for the social account model."""

    model = SocialAccount
    extra = 0
    fields = ["provider", "last_login", "date_joined"]
    readonly_fields = ["provider", "last_login", "date_joined"]

    def has_add_permission(self, request, obj):
        """Return False to prevent adding new social accounts."""
        return False


class AuthenticatorInline(admin.TabularInline):
    """Inline for the authenticator model."""

    model = Authenticator
    extra = 0
    fields = ["type", "created_at", "last_used_at"]
    readonly_fields = ["type", "created_at", "last_used_at"]

    def has_add_permission(self, request, obj):
        """Return False to prevent adding new authenticators."""
        return False


class UserSessionInline(admin.TabularInline):
    """Inline for the user session model."""

    model = UserSession
    extra = 0
    fields = [
        "created_at",
        "ip",
        "last_seen_at",
    ]
    readonly_fields = [
        "created_at",
        "ip",
        "last_seen_at",
    ]

    def has_add_permission(self, request, obj):
        """Return False to prevent adding new user sessions."""
        return False


@admin.register(PreferencesUser)
class PreferencesUserAdmin(UserAdmin):
    """Admin class for the preferences user model."""

    inlines = [EmailAddressInline, AuthenticatorInline, SocialAccountInline, UserSessionInline]
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined", "groups")
    readonly_fields = ["last_login", "date_joined"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "color_theme", "display_online", "email_notifications")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": (("last_login", "date_joined"),)}),
    )

    @cached_property
    def excluded_inlines(self):
        """Exclude inlines of which the corresponding app is not installed."""
        excluded = []
        if "allauth.mfa" not in settings.INSTALLED_APPS or Authenticator is None:
            excluded.append(AuthenticatorInline)
        if "allauth.socialaccount" not in settings.INSTALLED_APPS or SocialAccount is None:
            excluded.append(SocialAccountInline)
        if "allauth.usersessions" not in settings.INSTALLED_APPS or UserSession is None:
            excluded.append(UserSessionInline)
        if "allauth.account" not in settings.INSTALLED_APPS or EmailAddress is None:
            excluded.append(EmailAddressInline)
        return excluded

    def get_inlines(self, request, obj):
        """Return inlines excluding those that correspond to apps not installed."""
        inlines = super().get_inlines(request, obj)
        if obj is None:
            return []
        inlines = [x for x in inlines if x not in self.excluded_inlines]
        return inlines
