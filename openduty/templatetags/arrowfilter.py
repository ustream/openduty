from django.template import Library

import arrow

register = Library()

@register.filter
def arrowfilter(date, language='en'):
    if not date:
        return ''
    else:
        adate = arrow.get(date)
        return adate.humanize(locale=language)