from django.test import TestCase
from authenticator.management.commands.createlocalsuperuser import Command as CreateSuperUser
from authenticator.models import User
from StringIO import StringIO

class BasicTestCase(TestCase):
    def test_createsuperuser_management_command(self):
        "Check the operation of the createsuperuser management command"
        # We can use the management command to create a superuser
        new_io = StringIO()
        command = CreateSuperUser()
        command.execute(
            interactive=False,
            email='test@example.com',
            name='test',
            stdout=new_io,
        )
        command_output = new_io.getvalue().strip()
        self.assertEqual(command_output, 'Superuser created successfully.')
        u = User.objects.with_email('test@example.com')
        self.assertFalse(u.has_usable_password())

        # We can supress output on the management command
        new_io = StringIO()
        command.execute(
            interactive=False,
            email='test2@example.com',
            name='test2',
            verbosity=0,
            stdout=new_io,
        )
        command_output = new_io.getvalue().strip()
        self.assertEqual(command_output, '')
        u = User.objects.with_email('test2@example.com')
        self.assertFalse(u.has_usable_password())


class BasicUserTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(password='password')
        self.u2 = User.objects.create_user(password='password')

    def test_user_add_email(self):
        self.u1.add_email('u1@one.com')
        self.failUnless(User.objects.with_email('u1@one.com') == self.u1)
        self.u1.add_email('u1@two.com')
        self.failUnless(User.objects.with_email('u1@two.com') == self.u1)

    def test_add_blank_email(self):
        self.failIf(self.u1.authgroups.filter(email__isnull=True).count())
        self.u1.add_email('')
        self.failUnless(self.u1.authgroups.filter(email__isnull=True).count())

    def test_user_primary_group(self):
        self.u1.add_email('primary@test.com', primary=True)
        self.failUnless(self.u1.authgroups.get(email='primary@test.com').primary)

        self.u1.add_email('newprimary@test.com', primary=True)
        self.failIf(self.u1.authgroups.get(email='primary@test.com').primary)
        self.failUnless(self.u1.authgroups.get(email='newprimary@test.com').primary)

        self.u1.add_email('primary@test.com', primary=True)
        self.failIf(self.u1.authgroups.get(email='newprimary@test.com').primary)
        self.failUnless(self.u1.authgroups.get(email='primary@test.com').primary)

    def test_merge_users(self):
        self.u1.add_email('u1@test.com')
        self.u2.add_email('u2@test.com')
        self.u2.merge_into(self.u1)

        self.failUnless(User.objects.with_email('u2@test.com') == self.u1)

