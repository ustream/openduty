from django.utils import timezone
from openduty.models import Service, ServiceTokens, Token, SchedulePolicy, Incident
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APIClient
from .shared import BaseTestCase, random_string


class TestAPI(BaseTestCase):

    def setUp(self):
        super(TestAPI, self).setUp()
        self.sp = SchedulePolicy(name=random_string(), repeat_times=1)
        self.sp.save()
        self.service = Service(name=random_string(), policy=self.sp)
        self.service.save()
        self.token = Token(key="testtoken")
        self.token.save()
        self.servicetoken = ServiceTokens(name="testbinding", service_id=self.service, token_id=self.token)
        self.servicetoken.save()
        self.service2 = Service(name=random_string(), policy=self.sp)
        self.service2.save()
        self.token2 = Token(key="testtoken2")
        self.token2.save()
        self.servicetoken2 = ServiceTokens(name="testbinding", service_id=self.service2, token_id=self.token2)
        self.servicetoken2.save()

    def tearDown(self):
        super(TestAPI, self).tearDown()
        try:
            self.servicetoken.delete()
            self.servicetoken2.delete()
            self.token2.delete()
            self.token.delete()
            self.service2.delete()
            self.service.delete()
            self.sp.delete()
        except:
            pass

    def test_create_event(self):
        try:
            client = APIClient()
            response = client.post(
                '/api/create_event',
                data = {
                    "incident_key": "testing",
                    "service_key": self.token.key,
                    "event_type": "trigger",
                    "description": "test",
                    "details": "test"
                },
            )
            self.assertEqual(201, response.status_code)
            new_instance = Incident.objects.get(incident_key='testing')
            self.assertEqual("testing", new_instance.incident_key)
            self.assertEqual(Incident.TRIGGER, new_instance.event_type)
            self.assertEqual(self.service, new_instance.service_key)
        finally:
            pass

    def test_create_event_fails_with_invalid_key(self):
        try:
            client = APIClient()
            response = client.post(
                '/api/create_event',
                data = {
                    "incident_key": "testing",
                    "service_key": "invalid",
                    "event_type": "trigger",
                    "description": "test",
                    "details": "test"
                },
            )
            self.assertEqual(403, response.status_code)
        finally:
            pass


    def inject_incident(self):
        incident = Incident()
        incident.service_key = self.service
        incident.event_type = Incident.TRIGGER
        incident.incident_key = "testing"
        incident.description = "test"
        incident.details = "test"
        incident.occurred_at = timezone.now()
        incident.save()

    def test_create_event_different_service(self):
        self.inject_incident()
        try:
            client = APIClient()
            response = client.post(
                '/api/create_event',
                data = {
                    "incident_key": "testing",
                    "service_key": self.token2.key,
                    "event_type": "trigger",
                    "description": "test",
                    "details": "test"
                },
            )
            self.assertEqual(201, response.status_code)
            incidents = Incident.objects.all()
            self.assertEqual(2, incidents.count())
        finally:
            pass

    def test_incident_recovery(self):
        self.inject_incident()
        try:
            client = APIClient()
            response = client.post(
                '/api/create_event',
                data = {
                    "incident_key": "testing",
                    "service_key": self.token.key,
                    "event_type": "resolve",
                    "description": "test",
                    "details": "test"
                },
            )
            self.assertEqual(201, response.status_code)
            updated = Incident.objects.get(incident_key='testing')
            self.assertEqual(Incident.RESOLVE, updated.event_type)
        finally:
            updated.delete()

    def test_incident_acknowledge(self):
        self.inject_incident()
        try:
            client = APIClient()
            response = client.post(
                '/api/create_event',
                data = {
                    "incident_key": "testing",
                    "service_key": self.token.key,
                    "event_type": "acknowledge",
                    "description": "test",
                    "details": "test"
                },
            )
            self.assertEqual(201, response.status_code)
            updated = Incident.objects.get(incident_key='testing')
            self.assertEqual(Incident.ACKNOWLEDGE, updated.event_type)
        finally:
            updated.delete()