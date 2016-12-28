from authenticator.backends.local import LocalBackend
from authenticator.models import User
from django.test import TestCase

class LocalBackendTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user(password='password')
        self.u.add_email('user@test.com')
        self.u.add_email('user@test2.com')

    def test_authentication(self):
        backend = LocalBackend()
        u1 = backend.authenticate(password='password', email='user@test.com')
        u2 = backend.authenticate(password='password', email='user@test2.com')
        self.assertEqual(u1, self.u)
        self.assertEqual(u2, self.u)
