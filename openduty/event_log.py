__author__ = 'deathowl'

from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.conf import settings
from .models import EventLog, Service



@login_required()
def list(request):
    filtered_actions = ('notified', 'notification_failed')
    services = Service.objects.filter()
    events = EventLog.objects.exclude(action__in=filtered_actions).order_by('-occurred_at')
    page = request.GET.get('page')
    p = Paginator(events, settings.PAGINATION_DEFAULT_PAGINATION)
    try:
        paginated = p.page(page)
    except PageNotAnInteger:
        paginated = p.page(1)
    except EmptyPage:
        paginated = p.page(p.num_pages)
    return TemplateResponse(request, 'eventlog/list.html', {'services': services, 'events': paginated})

@login_required()
def get(request, id):
    services = Service.objects.all()
    page = request.GET.get('page')
    events = []
    actualService = None

    try:
        actualService = Service.objects.get(id = id)
        events = EventLog.objects.filter(service_key = actualService).order_by('-occurred_at')
    except Service.DoesNotExist:
        messages.error(request, "No such service!")

    p = Paginator(events, settings.PAGINATION_DEFAULT_PAGINATION)
    try:
        paginated = p.page(page)
    except PageNotAnInteger:
        paginated = p.page(1)
    except EmptyPage:
        paginated = p.page(p.num_pages)

    return TemplateResponse(request, 'eventlog/list.html', {'services': services, 'events' : paginated,
                                                            'actual' : actualService})