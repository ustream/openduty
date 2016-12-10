from __future__ import absolute_import

from notification.notifier.rocket import RocketNotifier
from openduty.celery import app
from notification.notifier.pushover import PushoverNotifier
from notification.notifier.xmpp import XmppNotifier
from notification.notifier.email import EmailNotifier
from notification.notifier.twilio_sms import TwilioSmsNotifier
from notification.notifier.twilio_call import TwilioCallNotifier
from notification.notifier.slack import SlackNotifier
from notification.notifier.prowl import ProwlNotifier

from notification.models import ScheduledNotification, UserNotificationMethod
from django.conf import settings
from django.utils import timezone

from openduty.models import EventLog

@app.task(ignore_result=True)
def send_notifications(notification_id):
    try:
        notification = ScheduledNotification.objects.get(id = notification_id)
        if notification.notifier == UserNotificationMethod.METHOD_XMPP:
            notifier = XmppNotifier(settings.XMPP_SETTINGS)
        if notification.notifier == UserNotificationMethod.METHOD_EMAIL:
            notifier = EmailNotifier(settings.EMAIL_SETTINGS)
        if notification.notifier == UserNotificationMethod.METHOD_TWILIO_SMS:
            notifier = TwilioSmsNotifier(settings.TWILIO_SETTINGS)
        if notification.notifier == UserNotificationMethod.METHOD_TWILIO_CALL:
            notifier = TwilioCallNotifier(settings.TWILIO_SETTINGS)
        if notification.notifier == UserNotificationMethod.METHOD_SLACK:
            notifier = SlackNotifier(settings.SLACK_SETTINGS)
        elif notification.notifier == UserNotificationMethod.METHOD_PUSHOVER:
            notifier = PushoverNotifier()
        elif notification.notifier == UserNotificationMethod.METHOD_PROWL:
            notifier = ProwlNotifier(settings.PROWL_SETTINGS)
        elif notification.notifier == UserNotificationMethod.METHOD_ROCKET:
            notifier = RocketNotifier()
        notifier.notify(notification)
        # Log successful notification
        logmessage = EventLog()
        if notification.incident:
            logmessage.service_key = notification.incident.service_key
            logmessage.incident_key = notification.incident
            logmessage.user = notification.user_to_notify
            logmessage.action = 'notified'
            logmessage.data = "Notification sent to %s about %s service" % (notification.user_to_notify, logmessage.service_key, )
            logmessage.occurred_at = timezone.now()
            logmessage.save()
        if notification.notifier != UserNotificationMethod.METHOD_TWILIO_CALL:
            # In case of a twilio call, we need the object for TWiml generation
            notification.delete()
    except ScheduledNotification.DoesNotExist:
        pass #Incident was resolved. NOP.
    except:
                # Log successful notification
        logmessage = EventLog()
        if notification.incident:
            logmessage.service_key = notification.incident.service_key
            logmessage.incident_key = notification.incident
            logmessage.user = notification.user_to_notify
            logmessage.action = 'notification_failed'
            logmessage.data = "Sending notification failed to %s about %s service" % (notification.user_to_notify, logmessage.service_key, )
            logmessage.occurred_at = timezone.now()
            logmessage.save()
        raise

