from rest_framework import viewsets, status
from openduty.serializers import OpsWeeklySerializer
from openduty.models import Incident
from openduty.models import Token
from openduty.models import ServiceTokens
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import dateutil.parser
from openduty.models import EventLog
from schedule.models import Calendar
from openduty import escalation_helper
from openduty.serializers import OnCallSerializer

__author__ = 'deathowl'


class OpsWeeklyIncidentViewSet(viewsets.ReadOnlyModelViewSet):

    """
    API endpoint that displays incidents in a format, that opsweekly can digest with ease
    """
    queryset = Incident.objects.none()
    serializer_class = OpsWeeklySerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        try:
            key = request.GET.get("service_key")
            if not key:
                return Response({}, status=status.HTTP_403_FORBIDDEN)
            token = Token.objects.get(key=key)
            servicetoken = ServiceTokens.objects.get(token_id=token)
            service = servicetoken.service_id
        except ServiceTokens.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        except Token.DoesNotExist:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        since = request.GET.get("since")
        until = request.GET.get("until")
        if not since or not until:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
        try:
            since = dateutil.parser.parse(since)
            until = dateutil.parser.parse(until)
        except ValueError:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

        events = EventLog.objects.filter(service_key=service).filter(action=Incident.TRIGGER).\
            filter(occurred_at__gt=since).filter(occurred_at__lt=until).order_by('occurred_at')
        page = self.paginate_queryset(events)
        if page is not None:
            response = []
            for event in page:
                r_row = {"occurred_at": event.occurred_at, "output": event.incident_key.details,
                         "incindent_key": event.incident_key.incident_key}
                response.append(r_row)
            serializer = self.get_serializer(response, many=True)
            return self.get_paginated_response(serializer.data)

        response = []
        for event in events:
            r_row = {"occurred_at": event.occurred_at, "output": event.incident_key.details,
                     "incindent_key": event.incident_key.incident_key}
            response.append(r_row)
        return Response(self.get_serializer(response, many=True).data)



class OpsWeeklyOnCallViewSet(viewsets.ReadOnlyModelViewSet):

    """
    API endpoint that displays incidents in a format, that opsweekly can digest with ease
    """
    queryset = Incident.objects.none()
    serializer_class = OnCallSerializer
    permission_classes = (AllowAny,)

    def retrieve(self, request, pk=None):
        try:
            sched = Calendar.objects.get(slug=pk)
        except Calendar.DoesNotExist:
            return Response({}, status.HTTP_404_NOT_FOUND)
        since = request.GET.get("since")
        until = request.GET.get("until")
        if not since or not until:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
        try:
            since = dateutil.parser.parse(since)
            until = dateutil.parser.parse(until)
        except ValueError:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

        currently_oncall_users = escalation_helper.get_events_users_inbetween(sched, since, until)
        return Response(self.get_serializer(currently_oncall_users, many=True).data)
