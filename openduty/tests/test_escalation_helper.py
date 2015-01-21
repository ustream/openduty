from schedule.models import Calendar, Event, Rule
from openduty.models import Service, SchedulePolicy, SchedulePolicyRule
from .shared import BaseTestCase, random_string
from django.utils import timezone
from datetime import timedelta
from openduty.escalation_helper import get_escalation_for_service

class TestGetEscalation(BaseTestCase):

    def setUp(self):
        super(TestGetEscalation, self).setUp()
        self.sp = SchedulePolicy(name=random_string(), repeat_times=1)
        self.sp.save()
        self.service = Service(name=random_string(), policy=self.sp)
        self.service.save()
        self.cal = Calendar(
            name=random_string(),
            slug=random_string(),
        )
        self.cal.save()
        self.spr = SchedulePolicyRule(
            schedule_policy=self.sp,
            position=0,
            schedule=self.cal,
            escalate_after=1,
        )
        self.spr.save()

    def tearDown(self):
        super(TestGetEscalation, self).tearDown()
        try:
            self.spr.delete()
            self.cal.delete()
            self.service.delete()
            self.sp.delete()
        except:
            pass

    def test_get_escalation_works_with_no_recurrence(self):
        event = Event(
            start = timezone.now() - timedelta(days=1),
            end = timezone.now() + timedelta(days=1),
            title = '{username},{username}'.format(username=self.username),
            calendar = self.cal,
        )
        event.save()
        try:
            events = get_escalation_for_service(self.service)
            self.assertEqual(2, len(events))
        finally:
            event.delete()

    def test_get_escalation_fails_with_no_recurrence_after_event_end(self):
        event = Event(
            start = timezone.now() - timedelta(days=2),
            end = timezone.now() - timedelta(days=1),
            title = '{username},{username}'.format(username=self.username),
            calendar = self.cal,
        )
        event.save()
        try:
            events = get_escalation_for_service(self.service)
            self.assertEqual(0, len(events))
        finally:
            event.delete()

    def test_get_escalation_empty_when_recurrance_is_not_now(self):
        rule = Rule(
            name=random_string(),
            description=random_string(),
            frequency='WEEKLY',
        )
        rule.save()
        # Active yesterday, and 1 week from now, but not today
        event = Event(
            start = timezone.now() - timedelta(days=2),
            end = timezone.now() - timedelta(days=1),
            title = '{username},{username}'.format(username=self.username),
            calendar = self.cal,
            rule = rule,
        )
        event.save()
        events = get_escalation_for_service(self.service)
        self.assertEqual(0, len(events))

    def test_get_escalation_works_when_recurrance_is_now(self):
        rule = Rule(
            name=random_string(),
            description=random_string(),
            frequency='WEEKLY',
        )
        rule.save()
        # Active last week at this time, recurring now
        event = Event(
            start = timezone.now() - timedelta(days=7, hours=5),
            end = timezone.now() + timedelta(hours=4) - timedelta(days=7),
            title = '{username},{username}'.format(username=self.username),
            calendar = self.cal,
            rule = rule,
        )
        event.save()
        events = get_escalation_for_service(self.service)
        self.assertEqual(2, len(events))

    def test_get_escalation_returns_empty_for_muted_services(self):
        event = Event(
            start = timezone.now() - timedelta(days=1),
            end = timezone.now() + timedelta(days=1),
            title = '{username},{username}'.format(username=self.username),
            calendar = self.cal,
        )
        event.save()
        self.service.notifications_disabled = True
        try:
            events = get_escalation_for_service(self.service)
            self.assertEqual(0, len(events))
        finally:
            event.delete()
