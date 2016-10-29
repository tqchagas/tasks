from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIClient


class BaseTestCase(TestCase):

    def setUp(self):
        self.email = 'usario@usuario.com'
        self.username = 'usuario'
        self.password = '12345'
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        self.data = {
            'username': self.username,
            'password': self.password
        } 

    def get_token(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/auth/', self.data, format='json')
        self.assertEqual(response.status_code, 200)
        return response.data.get('token')


class LoginTestCase(BaseTestCase):
    def setUp(self):
        return super(LoginTestCase, self).setUp()
    
    def test_login(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/auth/', self.data, format='json')
        token = self.get_token()
        self.assertEqual(response.status_code, 200)
