__author__ = 'deathowl'

from .models import User, SchedulePolicyRule, Service
from datetime import datetime, timedelta
from django.utils import timezone
from schedule.periods import Day


def get_current_events_users(calendar):
    now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
    result = []
    day = Day(calendar.events.all(), now)
    for o in day.get_occurrences():
        if o.start <= now <= o.end:
            usernames = o.event.title.split(',')
            for username in usernames:
                result.append(User.objects.get(username=username.strip()))
    return result


def get_escalation_for_service(service):
    result = []
    if service.notifications_disabled:
        return result
    rules = SchedulePolicyRule.getRulesForService(service)
    for item in rules:
        if item.schedule:
            result += get_current_events_users(item.schedule)
        if item.user_id:
            result.append(item.user_id)
    #TODO: This isnt de-deuped, is that right?
    return result

def services_where_user_is_on_call(user):
    from django.db.models import Q
    services = Service.objects.filter(
        Q(policy__rules__user_id=user) | Q(policy__rules__schedule__event__title__icontains=user)
    )
    return services
