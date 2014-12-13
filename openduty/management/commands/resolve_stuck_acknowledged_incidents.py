__author__ = 'deathowl'

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from openduty.models import Incident
import datetime


class Command(BaseCommand):
    help = 'Auto resolves stuck acknowledged incidents'
    def handle(self, *args, **options):
        limit = timezone.now() - datetime.timedelta(hours=12)
        entities = Incident.objects.filter(occurred_at__lte=limit).filter(event_type=Incident.ACKNOWLEDGE)
        for entity in entities:
            entity.event_type = Incident.RESOLVE
            entity.occured_at = timezone.now()
            entity.save()
            self.stdout.write('Stuck incident id:%s auto resolved because of 12 hours timeout' % entity.id)

        self.stdout.write('Stuck incidents autoresolved!')