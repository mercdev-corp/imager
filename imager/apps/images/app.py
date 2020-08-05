from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ImagesAppConfig(AppConfig):
    name = 'imager.apps.images'
    verbose_name = _('Images')
