__author__ = 'deathowl'

from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from notification.models import ScheduledNotification
from escalation_helper import services_where_user_is_on_call
from .models import Incident, Service, ServiceTokens, Token, EventLog, IncidentSilenced, ServiceSilenced
from rest_framework import viewsets
from .serializers import IncidentSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.core.exceptions import ValidationError
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notification.helper import NotificationHelper
from openduty.tasks import unsilence_incident
import uuid
import base64


class IncidentViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows incidents to be viewed or edited.
    """
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    def create(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(key = request.DATA["service_key"])
            serviceToken = ServiceTokens.objects.get(token_id=token)
            service = serviceToken.service_id
        except ServiceTokens.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        except Token.DoesNotExist:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        with transaction.atomic():
            try:
                incident = Incident.objects.get(incident_key=request.DATA["incident_key"], service_key=service)

                event_log_message = "%s api key changed %s from %s to %s" % (serviceToken.name, incident.incident_key, incident.event_type, request.DATA['event_type'])
            except (Incident.DoesNotExist, KeyError):
                incident = Incident()
                try:
                    incident.incident_key = request.DATA["incident_key"]
                except KeyError:
                    if request.DATA["event_type"] == Incident.TRIGGER:
                        incident.incident_key = base64.urlsafe_b64encode(uuid.uuid1().bytes).replace('=', '')
                    else:
                        response = {}
                        response["status"] = "failure"
                        response["message"] = "Mandatory parameter missing"
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                incident.service_key = service

                event_log_message = "%s api key created %s with status %s" % (serviceToken.name, incident.incident_key, request.DATA['event_type'])

            if incident.event_type != Incident.ACKNOWLEDGE or (incident.event_type == Incident.ACKNOWLEDGE and request.DATA["event_type"] == Incident.RESOLVE):
                event_log = EventLog()
                event_log.service_key = incident.service_key
                event_log.data = event_log_message
                event_log.occurred_at = timezone.now()
                event_log.save()

                incident.event_type = request.DATA["event_type"]
                incident.description = request.DATA["description"][:100]
                incident.details = request.DATA["details"]
                incident.occurred_at = timezone.now()
                try:
                    incident.full_clean()
                except ValidationError as e:
                    return Response({'errors': e.messages}, status=status.HTTP_400_BAD_REQUEST)
                incident.save()
                servicesilenced = ServiceSilenced.objects.filter(service=service).count() > 1
                if incident.event_type == Incident.TRIGGER and not servicesilenced:
                    NotificationHelper.notify_incident(incident)
                if incident.event_type == "resolve" or incident.event_type == Incident.ACKNOWLEDGE:
                    ScheduledNotification.remove_all_for_incident(incident)

            headers = self.get_success_headers(request.POST)

            response = {}
            response["status"] = "success"
            response["message"] = "Event processed"
            response["incident_key"] = incident.incident_key
            return Response(response, status=status.HTTP_201_CREATED, headers=headers)


@login_required()
def list(request, service_key = None):

    return process_list(request ,service_key, None ,'All incidents')

@login_required()
def unhandled(request, service_key = None):
    return process_list(request, service_key, Incident.TRIGGER, 'Unhandled incidents')

@login_required()
def acknowledged(request, service_key = None):
    return process_list(request, service_key, Incident.ACKNOWLEDGE, 'Current acknowledged incidents' )

@login_required()
def unhandled_for_on_call_user(request, service_key = None):
    services_to_list = services_where_user_is_on_call(request.user)

    if service_key is not None:
        converted_key = uuid.UUID(service_key)
        if converted_key in services_to_list:
            services_to_list = [converted_key]
        else:
            services_to_list = []
    return process_list(request, services_to_list , Incident.TRIGGER,
                        "Current unhandled incidents in services watched by me")

@login_required()
def process_list(request, service_key_or_key_list , event_type, title):

    services = Service.objects.all()
    if service_key_or_key_list is None:
        incidents = Incident.objects.all()
    elif isinstance(service_key_or_key_list, basestring):
        incidents = Incident.objects.filter(service_key = service_key_or_key_list)
    else:
        incidents = Incident.objects.filter(service_key__in = service_key_or_key_list)

    if event_type is not None:
        incidents = incidents.filter(event_type = event_type).order_by("-occurred_at")

    page = request.GET.get('page')

    paginator = Paginator(incidents, settings.PAGINATION_DEFAULT_PAGINATION)

    try:
        incidents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        incidents = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        incidents = paginator.page(paginator.num_pages)

    return TemplateResponse(request, 'incidents/list.html', {'incidents': incidents, 'title': title, 'url': request.get_full_path(), 'services': services })

@login_required()
def details(request, id):
    try:
        incident = Incident.objects.get(id = id)
        users = User.objects.all()
        return TemplateResponse(request, 'incidents/details.html', {'item': incident, 'users': users, 'url': request.get_full_path()})
    except Service.DoesNotExist:
        raise Http404

@login_required()
@require_http_methods(["POST"])
def update_type(request):
    try:
        with transaction.atomic():
            incident = Incident.objects.get(id = request.POST['id'])

            logmessage = EventLog()
            logmessage.service_key = incident.service_key
            logmessage.data = "%s changed %s from %s to %s" % (request.user.username, incident.incident_key, incident.event_type, request.POST['event_type'])
            logmessage.occurred_at = timezone.now()
            logmessage.save()

            incident.event_type = request.POST['event_type']
            incident.occurred_at = timezone.now()
            incident.save()

            if incident.event_type == Incident.RESOLVE or incident.event_type == Incident.ACKNOWLEDGE:
                ScheduledNotification.remove_all_for_incident(incident)

    except Incident.DoesNotExist:
        messages.error(request, 'Incident not found')
        return HttpResponseRedirect(request.POST['url'])
    except ValidationError as e:
        messages.error(request, e.messages)
    return HttpResponseRedirect(request.POST['url'])

@login_required()
@require_http_methods(["POST"])
def forward_incident(request):
    try:
        with transaction.atomic():
            incident = Incident.objects.get(id = request.POST['id'])
            user = User.objects.get(id = request.POST['user_id'])
            ScheduledNotification.remove_all_for_incident(incident)
            NotificationHelper.notify_user_about_incident(incident, user)
            event_log_message = "%s  changed assignee of incident :  %s  to %s" % (request.user.username, incident.incident_key, user.username)
            event_log = EventLog()
            event_log.service_key = incident.service_key
            event_log.data = event_log_message
            event_log.occurred_at = timezone.now()
            event_log.save()

    except Incident.DoesNotExist:
        messages.error(request, 'Incident not found')
        return HttpResponseRedirect(request.POST['url'])
    except User.DoesNotExist:
        messages.error(request, 'Incident not found')
        return HttpResponseRedirect(request.POST['url'])
    except ValidationError as e:
        messages.error(request, e.messages)
    return HttpResponseRedirect(request.POST['url'])


@login_required()
@require_http_methods(["POST"])
def silence(request, incident_id):
    try:
        incident = Incident.objects.get(id = incident_id)
        silence_for = request.POST.get('silence_for')
        url = request.POST.get("url")
        if IncidentSilenced.objects.filter(incident=incident).count() < 1:
            silenced_incident = IncidentSilenced()
            silenced_incident.incident = incident
            silenced_incident.silenced_until = timezone.now() + timezone.timedelta(hours=int(silence_for))
            silenced_incident.silenced = True
            silenced_incident.save()
            event_log_message = "%s silenced the of incident %s for %s hours" % (request.user.username, incident.incident_key, silence_for)
            event_log = EventLog()
            event_log.service_key = incident.service_key
            event_log.data = event_log_message
            event_log.occurred_at = timezone.now()
            event_log.save()
            ScheduledNotification.remove_all_for_incident(incident)
            incident.event_type = Incident.ACKNOWLEDGE
            incident.save()
            unsilence_incident.apply_async((incident_id,), eta=silenced_incident.silenced_until)
        return HttpResponseRedirect(url)
    except Service.DoesNotExist:
        raise Http404

