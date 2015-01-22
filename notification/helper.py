__author__ = 'deathowl'

from datetime import datetime, timedelta

from notification.tasks import send_notifications
from openduty.escalation_helper import get_escalation_for_service
from django.utils import timezone
from notification.models import ScheduledNotification
from django.conf import settings


class NotificationHelper(object):
    @staticmethod
    def notify_incident(incident):
        notifications = NotificationHelper.generate_notifications_for_incident(incident)

        for notification in notifications:
            notification.save()
            send_notifications.apply_async((notification.id,) ,eta=notification.send_at)
    @staticmethod
    def notify_user_about_incident(incident, user, delay=None, preparedmsg = None):
        notifications = NotificationHelper.generate_notifications_for_user(incident, user, delay, preparedmsg)

        for notification in notifications:
            notification.save()
            send_notifications.apply_async((notification.id,) ,eta=notification.send_at)

    @staticmethod
    def generate_notifications_for_incident(incident):
        now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
        duty_officers = get_escalation_for_service(incident.service_key)

        current_time = now

        notifications = []

        for officer_index, duty_officer in enumerate(duty_officers):
            escalation_time = incident.service_key.escalate_after * (officer_index + 1)
            escalate_at = current_time + timedelta(minutes=escalation_time)

            methods = duty_officer.notification_methods.order_by('position').all()
            method_index = 0

            for method in methods:
                notification_time = incident.service_key.retry * method_index + incident.service_key.escalate_after * officer_index
                notify_at = current_time + timedelta(minutes=notification_time)
                if notify_at < escalate_at:
                    notification = ScheduledNotification()
                    notification.incident = incident
                    notification.user_to_notify = duty_officer
                    notification.notifier = method.method
                    notification.send_at = notify_at
                    uri = settings.BASE_URL + "/incidents/details/" + str(incident.id)
                    notification.message = "A Service is experiencing a problem: " + incident.incident_key + " " + incident.description + ". Handle at: " + uri + " Details: " + incident.details

                    notifications.append(notification)

                    print "Notify %s at %s with method: %s" % (duty_officer.username, notify_at, notification.notifier)
                else:
                    break
                method_index += 1

            # todo: error handling

        return notifications

    @staticmethod
    def generate_notifications_for_user(incident, user, delay=None, preparedmsg = None):

        now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
        current_time = now
        notifications = []
        methods = user.notification_methods.order_by('position').all()
        method_index = 0

        for method in methods:
            if delay is None:
                notification_time = incident.service_key.retry * method_index + incident.service_key.escalate_after
            else:
                notification_time = method_index * delay
            notify_at = current_time + timedelta(minutes=notification_time)
            notification = ScheduledNotification()
            notification.incident = incident
            notification.user_to_notify = user
            notification.notifier = method.method
            notification.send_at = notify_at
            if preparedmsg is None:
                uri = settings.BASE_URL + "/incidents/details/" + str(incident.id)
                notification.message = "A Service is experiencing a problem: " + incident.incident_key + " " + incident.description + ". Handle at: " + uri
            else:
                notification.message = preparedmsg
            notifications.append(notification)
            print "Notify %s at %s with method: %s" % (user.username, notify_at, notification.notifier)
            method_index += 1

        # todo: error handling
        return notifications
