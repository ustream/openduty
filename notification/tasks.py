from __future__ import absolute_import

from openduty.celery import app
from notification.notifier.pushover import PushoverNotifier
from notification.notifier.xmpp import XmppNotifier
from notification.notifier.email import EmailNotifier
from notification.notifier.twilio_sms import TwilioSmsNotifier
from notification.notifier.twilio_call import TwilioCallNotifier
from notification.notifier.slack import SlackNotifier
from notification.models import ScheduledNotification, UserNotificationMethod
from django.conf import settings

@app.task(ignore_result=True)
def send_notifications(notification_id):
    try:
        notification = ScheduledNotification.objects.get(id = notification_id)
        if notification.notifier == UserNotificationMethod.METHOD_XMPP:
            notifier = XmppNotifier(settings.XMPP_SETTINGS)
        if notification.notifier == UserNotificationMethod.METHOD_EMAIL:
            notifier = EmailNotifier(settings.XMPP_SETTINGS)
        if notification.notifier == UserNotificationMethod.METHOD_TWILIO_SMS:
            notifier = TwilioSmsNotifier(settings.TWILIO_SETTINGS)
        if notification.notifier == UserNotificationMethod.METHOD_TWILIO_CALL:
            notifier = TwilioCallNotifier(settings.TWILIO_SETTINGS)
        if notification.notifier == UserNotificationMethod.METHOD_SLACK:
            notifier = SlackNotifier(settings.SLACK_SETTINGS)
        elif notification.notifier == UserNotificationMethod.METHOD_PUSHOVER:
            notifier = PushoverNotifier()
        notifier.notify(notification)
        notification.delete()
    except ScheduledNotification.DoesNotExist:
        pass #Incident was resolved. NOP.

