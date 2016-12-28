from django.test import TestCase
from django.core import mail
from activator.models import ActivationReusedException
from activator.tests.mockapp.models import User, SimpleRequest

class ModelTests(TestCase):
    def setUp(self):
        self.u = User.objects.create(email='user@test.com', password='password')

    def test_no_email_given(self):
        SimpleRequest.objects.request(self.u)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.u.email])

    def test_email_given(self):
        SimpleRequest.objects.request(self.u, 'other@test.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['other@test.com'])

    def test_use(self):
        self.failIf(self.u.is_active)
        request = SimpleRequest.objects.request(self.u)
        request.use(None)
        self.failUnless(self.u.is_active)

    def test_reuse(self):
        request = SimpleRequest.objects.request(self.u)
        request.use(None)
        self.failUnlessRaises(request.use, None, ActivationReusedException)
