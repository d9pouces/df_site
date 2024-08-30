"""Python functions to provide Django settings depending on other settings."""

from typing import Any, Optional


def allauth_signup_form(values: dict[str, Any]) -> Optional[str]:
    """Return the form class to use for signing up."""
    if values.get("RECAPTCHA_PRIVATE_KEY") and values.get("RECAPTCHA_PUBLIC_KEY"):
        return "df_site.users.forms.ReCaptchaForm"
    return None


allauth_signup_form.required_settings = ["RECAPTCHA_PRIVATE_KEY", "RECAPTCHA_PUBLIC_KEY"]
