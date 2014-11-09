import unittest
from django.test import Client
import string
import random
from django.contrib.auth import models as auth_models

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = random_string()
        cls.password = random_string()
        cls.user = auth_models.User.objects.create_superuser(
            cls.username,
            'test@localhost',
            cls.password,
        )

    @classmethod
    def tearDownClass(cls):
        try:
            cls.user.delete()
        except:
            pass

class LoggedInTestCase(BaseTestCase):

    def setUp(self):
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
