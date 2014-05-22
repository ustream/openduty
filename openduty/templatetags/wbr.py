import string
from django.template.defaultfilters import stringfilter, register
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


@register.filter(needs_autoescape=True)
@stringfilter
def wbr(value, what, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    parts = string.split(value, what)

    safe_parts = map(esc, parts)

    result = string.join(safe_parts, what + '<wbr/>')

    return mark_safe(result)

register.filter('wbr', wbr)