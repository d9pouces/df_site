"""Django settings for the project."""

from df_site.defaults import *  # noqa F403

DF_INDEX_VIEW = "paint_manager.views.IndexView"
DF_SITE_TITLE = "Peintures à maquette"
DF_SITE_DESCRIPTION = "Gestion des peintures en stock"
DF_SITE_KEYWORDS = ["Tamiya", "Humbroll", "Gunze"]
DF_SITE_AUTHOR = "d9pouces"
DF_SITE_ORGANIZATION = "d9pouces"
DF_SITE_SOCIAL_NETWORKS = {
    "instagram": "https://www.instagram.com/d9pouces/",
    "twitter": "https://x.com/d9pouces/",
    "github": "https://github.com/d9pouces/",
}
DF_INSTALLED_APPS.insert(0, "paint_manager")  # noqa F405
AUTH_USER_MODEL = "paint_manager.PaintOwner"
AUTH_USER_SETTINGS_VIEW = "paint_manager.views.CustomUserSettingsView"
DF_TEMPLATE_CONTEXT_PROCESSORS.append("paint_manager.context_processors.search_infos")  # noqa F405
