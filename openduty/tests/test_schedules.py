from django.core.urlresolvers import reverse
from schedule.models import Calendar
from .shared import LoggedInTestCase, random_string

class TestSchedulesViews(LoggedInTestCase):

    def setUp(self):
        super(TestSchedulesViews, self).setUp()
        self.cal = Calendar(
            name=random_string(),
            slug=random_string(),
        )
        self.cal.save()

    def tearDown(self):
        super(TestSchedulesViews, self).tearDown()
        try:
            self.cal.delete()
        except:
            pass

    def test_schedule_detail_view_works_with_query_args(self):
        response = self.client.get(
            reverse('openduty.schedules.details', args=[self.cal.id]),
            {'month': '11', 'year': '2014'},
        )
        self.assertEqual(response.status_code, 200)
