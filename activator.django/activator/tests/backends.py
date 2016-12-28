from datetime import datetime, timedelta
from django.test import TestCase

from activator.tests.mockapp.models import User, SimpleRequest
from activator.backends import TokenBackend


class TokenBackendTests(TestCase):
    def setUp(self):
        self.u = User.objects.create(email='user@test.com', password='password')
        self.backend = TokenBackend()

    def test_authentication(self):
        request = SimpleRequest.objects.request(self.u)
        user = self.backend.authenticate(type=SimpleRequest, token=request.token)
        self.assertEqual(user, self.u)

    def test_used(self):
        request = SimpleRequest.objects.request(self.u)
        request.used = datetime.now()
        request.save()
        user = self.backend.authenticate(type=SimpleRequest, token=request.token)
        self.assertEqual(user, None)

    def test_expired(self):
        request = SimpleRequest.objects.request(self.u)
        request.sent = datetime.now() - timedelta(1) - SimpleRequest.timeframe
        request.save()
        user = self.backend.authenticate(type=SimpleRequest, token=request.token)
        self.assertEqual(user, None)
