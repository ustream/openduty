__author__ = 'deathowl'

from time import sleep, time
import datetime
from openduty.serializers import NoneSerializer
from openduty.models import Incident
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .celery import add
from random import randint



class HealthCheckViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = NoneSerializer

    def list(self, request):
        try:
           firstincident = Incident.objects.first()
        except Exception:
            return Response("FAILED", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response("OK", status=status.HTTP_200_OK)


class CeleryHealthCheckViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = NoneSerializer
    
    def list(self, request):
        try:
            timestamp = int(time())
            random = randint(0, 100000)
            result = add.apply_async(args=[timestamp, random])
            now = datetime.datetime.now()
            while (now + datetime.timedelta(seconds=10)) > datetime.datetime.now():
                if result.result == timestamp + random:
                    return Response("OK", status=status.HTTP_200_OK)
                sleep(0.5)
        except IOError:
            pass
        return Response("FAILED", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
