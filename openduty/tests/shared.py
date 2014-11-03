import unittest
from django.test import Client
import string
import random
from django.contrib.auth import models as auth_models

def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class LoggedInTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.username = string_generator()
        cls.password = string_generator()
        cls.user = auth_models.User.objects.create_superuser(
            cls.username,
            'test@localhost',
            cls.password,
        )
        cls.client.login(username=cls.username, password=cls.password)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.user.delete()
        except:
            pass

