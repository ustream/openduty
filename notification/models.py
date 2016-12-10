import datetime
import dateutil
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext_lazy as _
from openduty.models import Incident


@python_2_unicode_compatible
class UserNotificationMethod(models.Model):
    """
    Schedule rule
    """

    METHOD_TWILIO_SMS = 'twilio_sms'
    METHOD_TWILIO_CALL = 'twilio_call'
    METHOD_EMAIL = 'email'
    METHOD_PUSHOVER = 'pushover'
    METHOD_XMPP = 'xmpp'
    METHOD_SLACK = 'slack'
    METHOD_PROWL = 'prowl'
    METHOD_ROCKET = 'rocket'


    methods = [METHOD_XMPP, METHOD_PUSHOVER, METHOD_EMAIL, METHOD_TWILIO_SMS, METHOD_TWILIO_CALL, METHOD_SLACK, METHOD_PROWL, METHOD_ROCKET]

    user = models.ForeignKey(User, related_name='notification_methods')
    position = models.IntegerField()
    method = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('user_notification_method')
        verbose_name_plural = _('user_notification_methods')
        db_table = 'openduty_usernotificationmethod'

    def __str__(self):
        return str(self.id)


@python_2_unicode_compatible
class ScheduledNotification(models.Model):
    notifier = models.CharField(max_length=30)
    message = models.CharField(max_length=500)
    user_to_notify = models.ForeignKey(User)
    send_at = models.DateTimeField()
    incident = models.ForeignKey(Incident, blank=True, null=True, default=None)

    class Meta:
        verbose_name = _('scheduled_notifications')
        verbose_name_plural = _('scheduled_notifications')
        db_table = 'openduty_schedulednotification'

    def __str__(self):
        return str(self.id)

    @staticmethod
    def remove_all_for_incident(incident):
        notices = ScheduledNotification.objects.filter(incident=incident)
        for notice in notices:
            notice.delete()

    @staticmethod
    def get_notifications_to_send(date=None):
        if not date:
            date = datetime.datetime.now(dateutil.tz.tzutc())
        return ScheduledNotification.objects.filter(send_at__lte=date)

