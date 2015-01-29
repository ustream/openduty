from django.utils import timezone

__author__ = 'deathowl'

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from .models import Service, ServiceTokens, SchedulePolicy, Token, User, ServiceSilenced, Incident
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.contrib import messages
from openduty.tasks import unsilence_incident



@login_required()
def list(request):
    services = Service.objects.all();
    return TemplateResponse(request, 'services/list.html', {'services': services})

@login_required()
def delete(request, id):
    try:
        service = Service.objects.get(id = id)
        service.delete()
        return HttpResponseRedirect('/services/');
    except Service.DoesNotExist:
        raise Http404

@login_required()
def edit(request, id):
    try:
        service = Service.objects.get(id = id)
        try:
            api_keys = ServiceTokens.objects.filter(service_id = service)
        except ServiceTokens.DoesNotExist:
            api_keys = []

        policy = service.policy if service.policy else None
        all_polcies = SchedulePolicy.objects.all()
        return TemplateResponse(request, 'services/edit.html', {
            'item': service,
            'policy': policy,
            'policies': all_polcies,
            'api_keys': api_keys
        })
    except Service.DoesNotExist:
        raise Http404

@login_required()
def new(request):
    all_policies = SchedulePolicy.objects.all()
    return TemplateResponse(request, 'services/edit.html', {'policies': all_policies})

@login_required()
@require_http_methods(["POST"])
def save(request):
    # Update service fields
    try:
        service = Service.objects.get(id = request.POST['id'])
    except Service.DoesNotExist:
        service = Service()

    service.name = request.POST['name']
    service.escalate_after = request.POST['escalate_after']
    service.retry = request.POST['retry']
    service.notifications_disabled = request.POST.get("disable_notification", "off") == "on"
    if(request.POST['policy']):
        pol = SchedulePolicy.objects.get(id = request.POST['policy'])
    else:
        pol = None
    service.policy = pol
    # Save service
    try:
        service.save()
    except IntegrityError:
        messages.error(request, 'Service validation failed')
        if len (request.POST['id']) > 0:
            return HttpResponseRedirect(reverse('openduty.services.edit', None, [str(request.POST['id'])]))
        else:
            return HttpResponseRedirect(reverse('openduty.services.new'))

    return HttpResponseRedirect('/services/');

@login_required()
def token_delete(request, token_id):
    try:
        token = ServiceTokens.objects.get(id = token_id)
        token.delete()
        return HttpResponseRedirect(reverse('openduty.services.edit', None, [str(token.service_id.id)]));
    except Service.DoesNotExist:
        raise Http404

@login_required()
@require_http_methods(["POST"])
def token_create(request, service_id):
    try:
        service = Service.objects.get(id = service_id)
        token = Token()
        token.save()
        service_token = ServiceTokens.objects.create(service_id = service, token_id = token, name=request.POST['key_name'])
        service_token.save()
        return HttpResponseRedirect(reverse('openduty.services.edit', None, [str(service_id)]));
    except Service.DoesNotExist:
        raise Http404

@login_required()
@require_http_methods(["POST"])
def silence(request, service_id):
    try:
        service = Service.objects.get(id = service_id)
        silence_for = request.POST.get('silence_for')
        url = request.POST.get("url")
        if ServiceSilenced.objects.filter(service=service).count() < 1:
            silenced_service = ServiceSilenced()
            silenced_service.service = service
            silenced_service.silenced_until = timezone.now() + timezone.timedelta(hours=int(silence_for))
            silenced_service.silenced = True
            silenced_service.save()
            unsilence_service.apply_async((service_id,), eta=silenced_service.silenced_until)
        return HttpResponseRedirect(url)
    except Service.DoesNotExist:
        raise Http404
