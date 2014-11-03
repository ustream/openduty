from django.core.urlresolvers import reverse
from schedule.models import Calendar, Event, Rule
from .shared import LoggedInTestCase, string_generator
from datetime import timedelta
from django.utils import timezone

class TestEventViews(LoggedInTestCase):

    def setUp(self):
        super(TestEventViews, self).setUp()
        self.cal = Calendar(
            name=string_generator(),
            slug=string_generator(),
        )
        self.cal.save()
        self.event = Event(
            start=timezone.now(),
            end=timezone.now() + timedelta(weeks=6),
            title=string_generator(),
            calendar=self.cal,
        )
        self.event.save()

    def tearDown(self):
        super(TestEventViews, self).tearDown()
        try:
            self.cal.delete()
            self.event.delete()
        except:
            pass

    def test_event_can_be_recurring(self):
        from dateutil.rrule import WEEKLY
        rule = Rule(
            name=string_generator(),
            description=string_generator(),
            frequency=WEEKLY,
        )
        rule.save()
        try:
            url = reverse(
                'openduty.events.create_or_edit_event',
                kwargs = {
                    'calendar_slug': self.cal.slug,
                    'event_id': str(self.event.id),
                },
            )
            response = self.client.post(
                path = url,
                data = {
                    "start_0": self.event.start.strftime('%Y-%m-%d'),
                    "start_1": "09:00",
                    "end_0": self.event.end.strftime('%Y-%m-%d'),
                    "end_1": "23:00",
                    "description": "desc",
                    "rule": str(rule.id),
                    "oncall": "foo",
                    "fallback": "bar",
                },
            )
            self.assertEqual(302, response.status_code)
            e = Event.objects.get(id=self.event.id)
            self.assertEqual(rule, e.rule)
        finally:
            rule.delete()
