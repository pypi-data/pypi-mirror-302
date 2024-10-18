from django.conf import settings
from django.utils.module_loading import import_string

__all__ = ["DJANGO_SETTINGS_PARAM", "use_constance", "multirate_throttling_config"]

DJANGO_SETTINGS_PARAM = "MULTIRATE_THROTTLING_USE_CONSTANCE"

use_constance = getattr(settings, DJANGO_SETTINGS_PARAM, False)
multirate_throttling_config = (
    import_string("constance.config")
    if use_constance
    else import_string("rest_framework.settings.api_settings")
)
