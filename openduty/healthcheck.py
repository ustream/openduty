__author__ = 'deathowl'

from openduty.serializers import NoneSerializer
from openduty.models import Incident
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets



class HealthCheckViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = NoneSerializer
    def list(self, request):
        try:
           firstincident = Incident.objects.first()
        except Exception:
            return Response("FAILED", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response("OK", status=status.HTTP_200_OK)

