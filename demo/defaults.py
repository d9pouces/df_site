"""Django settings for the project."""

from df_site.defaults import *  # noqa F403

DF_INDEX_VIEW = "demo.views.IndexView"
DF_SITE_TITLE = "Technological proof of concept"
DF_SITE_DESCRIPTION = "This is a technological proof of concept."
DF_SITE_KEYWORDS = ["Django", "Bootstrap", "WebSockets", "HTMX", "Django Channels"]
DF_SITE_AUTHOR = "d9pouces"
DF_SITE_ORGANIZATION = "d9pouces"
DF_SITE_SOCIAL_NETWORKS = {
    "instagram": "https://www.instagram.com/d9pouces/",
    "twitter": "https://x.com/d9pouces/",
    "github": "https://github.com/d9pouces/",
}
DF_INSTALLED_APPS.insert(0, "demo")  # noqa F405
