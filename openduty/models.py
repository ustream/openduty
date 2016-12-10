__author__ = 'deathowl'

import uuid
import hmac
from hashlib import sha1

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from uuidfield import UUIDField
from django.core.exceptions import ValidationError
from schedule.models import Calendar
from django.contrib.auth import models as auth_models
from django.db.models import signals
from django.conf import settings


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

@python_2_unicode_compatible
class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        unique = uuid.uuid4()
        return hmac.new(unique.bytes, digestmod=sha1).hexdigest()

    def __unicode__(self):
        return self.key

    def __str__(self):
        return self.key


@python_2_unicode_compatible
class SchedulePolicy(models.Model):
    """
    Schedule policy
    """
    name = models.CharField(max_length=80, unique=True)
    repeat_times = models.IntegerField()

    class Meta:
        verbose_name = _('schedule_policy')
        verbose_name_plural = _('schedule_policies')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name)


@python_2_unicode_compatible
class Service(models.Model):
    """
    Incidents are representations of a malfunction in the system.
    """
    name = models.CharField(max_length=80, unique=True)
    id = UUIDField(primary_key=True, auto=True)
    retry = models.IntegerField(blank=True, null=True)
    policy = models.ForeignKey(SchedulePolicy, blank=True, null=True)
    escalate_after = models.IntegerField(blank=True, null=True)
    notifications_disabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('service')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.id)

@python_2_unicode_compatible
class EventLog(models.Model):
    """
    Event Log
    """
    ACTIONS = (('acknowledge', 'acknowledge'),
               ('resolve', 'resolve'),
               ('silence_service', 'silence service'),
               ('unsilence_service', 'unsilence service'),
               ('silence_incident', 'silence incident'),
               ('unsilence_incident', 'unsilence incident'),
               ('forward', 'forward'),
               ('log', 'log'),
               ('notified','notified'),
               ('notification_failed', 'notification failed'),
               ('trigger', 'trigger'))

    @property
    def color(self):
        colort_dict = {'acknowledge': 'warning',
                       'resolve': 'success',
                       'silence_service': 'active',
                       'unsilence_service': 'active',
                       'silence_incident': 'active',
                       'unsilence_incident': 'active',
                       'forward': 'info',
                       'trigger': 'trigger',
                       'notified': 'success',
                       'notification_failed': 'danger',
                       'log': ''}
        return colort_dict[self.action]

    user = models.ForeignKey(User, blank=True, default=None, null=True, related_name='users')
    incident_key = models.ForeignKey('Incident', blank=True, null=True)
    action = models.CharField(choices=ACTIONS, default='log', max_length="100")
    service_key = models.ForeignKey(Service)
    data = models.TextField()
    occurred_at = models.DateTimeField()
    class Meta:
        verbose_name = _('eventlog')
        verbose_name_plural = _('eventlog')

    def __str__(self):
        return self.data

    def natural_key(self):
        return (self.service_key, self.id)


@python_2_unicode_compatible
class Incident(models.Model):
    TRIGGER = "trigger"
    RESOLVE = "resolve"
    ACKNOWLEDGE = "acknowledge"
    """
    Incidents are representations of a malfunction in the system.
    """
    service_key = models.ForeignKey(Service)
    incident_key = models.CharField(max_length=200)
    event_type = models.CharField(max_length=15)
    description = models.CharField(max_length=200)
    details = models.TextField()
    occurred_at = models.DateTimeField()

    @property
    def color(self):
        colort_dict = {'acknowledge': 'warning',
                       'resolve': 'success',
                       'silence_service': 'active',
                       'silence_incident': 'active',
                       'forward': 'info',
                       'trigger': 'trigger',
                       'log': ''}
        return colort_dict[self.event_type]

    class Meta:
        verbose_name = _('incidents')
        verbose_name_plural = _('incidents')
        unique_together = (("service_key", "incident_key"),)

    def __str__(self):
        return self.incident_key

    def natural_key(self):
        return (self.service_key, self.incident_key)
    def clean(self):
        if self.event_type not in ['trigger', 'acknowledge', 'resolve']:
            raise ValidationError("'%s' is an invalid event type, valid values are 'trigger', 'acknowledge' and 'resolve'" % self.event_type)

@python_2_unicode_compatible
class ServiceTokens(models.Model):
    """
    Service tokens
    """
    name = models.CharField(max_length=80)
    service_id = models.ForeignKey(Service)
    token_id = models.ForeignKey(Token)

    class Meta:
        verbose_name = _('service_tokens')
        verbose_name_plural = _('service_tokens')

    def __str__(self):
        return self.name




@python_2_unicode_compatible
class SchedulePolicyRule(models.Model):
    """
    Schedule rule
    """
    schedule_policy = models.ForeignKey(SchedulePolicy, related_name='rules')
    position = models.IntegerField()
    user_id = models.ForeignKey(User, blank=True, null=True)
    schedule = models.ForeignKey(Calendar, blank=True, null=True)
    escalate_after = models.IntegerField()

    class Meta:
        verbose_name = _('schedule_policy_rule')
        verbose_name_plural = _('schedule_policy_rules')

    def __str__(self):
        return str(self.id)

    @classmethod
    def getRulesForService(cls, service):
        return cls.objects.filter(schedule_policy=service.policy)

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    phone_number = models.CharField(max_length=50)
    pushover_user_key = models.CharField(max_length=50)
    pushover_app_key = models.CharField(max_length=50)
    slack_room_name = models.CharField(max_length=50)
    prowl_api_key = models.CharField(max_length=50, blank=True)
    prowl_application = models.CharField(max_length=256, blank=True)
    prowl_url = models.CharField(max_length=512, blank=True)
    rocket_webhook_url = models.CharField(max_length=512, blank=True)

class ServiceSilenced(models.Model):
    service = models.ForeignKey(Service)
    silenced = models.BooleanField(default=False)
    silenced_until = models.DateTimeField()


class IncidentSilenced(models.Model):
    incident = models.ForeignKey(Incident)
    silenced = models.BooleanField(default=False)
    silenced_until = models.DateTimeField()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)

signals.post_syncdb.disconnect(
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser')
