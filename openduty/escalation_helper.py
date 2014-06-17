__author__ = 'deathowl'

from .models import User, SchedulePolicyRule, Service
from datetime import datetime
from django.utils import timezone


def get_escalation_for_service(service):
    result = []
    rules = SchedulePolicyRule.getRulesForService(service)
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

def services_where_user_is_on_call(user):
    result = []

    for service in Service.objects.all():
        escalation_users = map(lambda user: user.id, get_escalation_for_service(service))
        print escalation_users
        if user.id in escalation_users:
            result.append(service.id)

    return result