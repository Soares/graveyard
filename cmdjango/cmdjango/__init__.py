from cm import Converter, FileLoader
from django.conf import settings
import functions, elements

from django.contrib.sites.models import Site
context = {
    'site': Site.objects.get_current(),
    'images': settings.IMAGE_BASE,
    'media': settings.MEDIA_URL,
    'email': settings.EMAIL_SENDER,
}
manager = FileLoader(settings.CM_DIR, settings.HTML_DIR)
converter = Converter(manager, context=context, optimize=True, compress=not settings.DEBUG)
converter.elements.append(elements.library)
converter.functions.append(functions.library)
