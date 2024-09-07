"""Python functions to provide Django settings depending on other settings."""

import os
from typing import Any, Optional


def allauth_signup_form(values: dict[str, Any]) -> Optional[str]:
    """Return the form class to use for signing up."""
    if values.get("RECAPTCHA_PRIVATE_KEY") and values.get("RECAPTCHA_PUBLIC_KEY"):
        return "df_site.users.forms.ReCaptchaForm"
    return None


allauth_signup_form.required_settings = ["RECAPTCHA_PRIVATE_KEY", "RECAPTCHA_PUBLIC_KEY"]


def are_tests_running(values: dict[str, Any]) -> bool:
    """Return True if we are running unit tests."""
    return "testserver" in values.get("ALLOWED_HOSTS", [])


are_tests_running.required_settings = ["ALLOWED_HOSTS"]


def load_tox_environment():
    """Is a workaround for https://github.com/tox-dev/tox-docker/issues/55."""
    if os.environ.get("REDIS_HOST") and os.environ.get("REDIS_6379_TCP_PORT"):
        os.environ["REDIS_URL"] = f'redis://:p_df_site@{os.environ["REDIS_HOST"]}:{os.environ["REDIS_6379_TCP_PORT"]}/1'
    if os.environ.get("POSTGRES_HOST") and os.environ.get("POSTGRES_5432_TCP_PORT"):
        os.environ["DATABASE_URL"] = (
            f'postgresql://u_df_site:p_df_site@{os.environ["POSTGRES_HOST"]}:'
            f'{os.environ["POSTGRES_5432_TCP_PORT"]}/d_df_site'
        )
    if os.environ.get("MINIO_HOST") and os.environ.get("MINIO_9000_TCP_PORT"):
        os.environ["MAIN_STORAGE_DIR"] = (
            f's3:http://u_df_site:p_df_site@127.0.0.1:' f'{os.environ["MINIO_9000_TCP_PORT"]}/f_df_site'
        )
