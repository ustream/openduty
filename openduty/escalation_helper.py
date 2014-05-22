__author__ = 'deathowl'

from .models import User, SchedulePolicyRule
from datetime import datetime
from django.utils import timezone


def get_escalation_for_service(service):
    result = []
    serv = service
    rules = SchedulePolicyRule.objects.filter(schedule_policy=serv.policy)
    now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
    for item in rules:
        if item.schedule:
            events = item.schedule.events.filter(start__lte=now).filter(end__gte=now)
            for event in events:
                usernames = event.title.split(',')
                for username in usernames:
                    result.append(User.objects.get(username=username.strip()))
        if item.user_id:
            result.append(item.user_id)
    return result