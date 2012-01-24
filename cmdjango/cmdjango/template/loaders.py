from django.conf import settings
from django.template import TemplateDoesNotExist
from cmdjango import converter
from cm.exceptions import ConversionError, FileNotFound

def convert_template(template_name, template_dirs=None):
    if template_name.endswith('.html'):
        lookup_name = template_name[:-5]
    elif template_name.endswith('.txt'):
        lookup_name = template_name[:-4]
    else:
        lookup_name = template_name
    try:
        filename = converter.convert(lookup_name, template_name)
    except (ConversionError, FileNotFound):
        error_msg = 'Tried %s in %s' % (template_name, settings.CM_IN_DIR)
        raise TemplateDoesNotExist(error_msg)
    return (open(filename).read().decode(settings.FILE_CHARSET), filename)
convert_template.is_usable = True
