__author__ = 'deathowl'

from .models import User, SchedulePolicyRule, Service
from datetime import datetime, timedelta
from django.utils import timezone


def get_escalation_for_service(service):
    result = []
    if service.notifications_disabled:
        return result
    rules = SchedulePolicyRule.getRulesForService(service)
    now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
    for item in rules:
        if item.schedule:
            events = item.schedule.events.all()
            for event in events:
                if event.rule:
                    #TODO: This assumes no more than monthly occurance. There
                    # must be a better way to ask an event if x date falls within
                    # an occurence
                    for o in event.get_occurrences(now, now+timedelta(days=32)):
                        if o.start <= now <= o.end:
                            usernames = event.title.split(',')
                            for username in usernames:
                                result.append(User.objects.get(username=username.strip()))
                            break
                elif event.start <= now <= event.end:
                    usernames = event.title.split(',')
                    for username in usernames:
                        result.append(User.objects.get(username=username.strip()))
        if item.user_id:
            result.append(item.user_id)
    #TODO: This isnt de-deuped, is that right?
    return result

def services_where_user_is_on_call(user):
    result = []

    for service in Service.objects.all():
        escalation_users = map(lambda user: user.id, get_escalation_for_service(service))
        if user.id in escalation_users:
            result.append(service.id)

    return result
