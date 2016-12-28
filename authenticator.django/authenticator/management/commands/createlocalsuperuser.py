"""
Management utility to create superusers.
"""

import getpass
import re
import sys
from optparse import make_option
from django.core import exceptions
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from authenticator.models import User

EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain

def is_valid_email(value):
    if not EMAIL_RE.search(value):
        raise exceptions.ValidationError(_('Invalid email address.'))
    try:
        User.objects.with_email(value)
    except User.DoesNotExist:
        return
    raise exceptions.ValidationError(_('This email is already in use.'))

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--email', dest='email', default=None,
            help='Specifies the email for the superuser.'),
        make_option('--name', dest='name', default=None,
            help='Specifies the name for the superuser.'),
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help=('Tells Django to NOT prompt the user for input of any kind. '
                  'You must use --name and --email with --noinput, and '
                  'superusers created with --noinput will not be able to log '
                  'in until they\'re given a valid password.')),
    )
    help = 'Used to create a superuser.'

    def handle(self, *args, **options):
        name = options.get('name', None)
        email = options.get('email', None)
        interactive = options.get('interactive')
        verbosity = int(options.get('verbosity', 1))

        # If not provided, create the user with an unusable password
        password = None

        # Try to determine the current system user's name to use as a default.
        try:
            default_name = getpass.getuser().replace(' ', '').lower()
        except (ImportError, KeyError):
            # KeyError will be raised by os.getpwuid() (called by getuser())
            # if there is no corresponding entry in the /etc/passwd file
            # (a very restricted chroot environment, for example).
            default_name = ''

        # Prompt for name/password. Enclose this whole thing in a
        # try/except to trap for a keyboard interrupt and exit gracefully.
        if interactive:
            try:
                # Get an email
                while 1:
                    if not email:
                        email = raw_input('E-mail address: ')
                    try:
                        is_valid_email(email)
                    except exceptions.ValidationError as e:
                        sys.stderr.write(e.msg.strip() + '\n')
                        email = None
                    else:
                        break

                # Get a name
                if not name:
                    input_msg = 'Name'
                    if default_name:
                        input_msg += ' (Leave blank to use %r)' % default_name
                    name = raw_input(input_msg + ': ')
                if default_name and name == '':
                    name = default_name

                # Get a password
                while 1:
                    if not password:
                        password = getpass.getpass()
                        password2 = getpass.getpass('Password (again): ')
                        if password != password2:
                            sys.stderr.write("Error: Your passwords didn't match.\n")
                            password = None
                            continue
                    if password.strip() == '':
                        sys.stderr.write("Error: Blank passwords aren't allowed.\n")
                        password = None
                        continue
                    break
            except KeyboardInterrupt:
                sys.stderr.write("\nOperation cancelled.\n")
                sys.exit(1)

        user = User.objects.create_superuser(password, name)
        user.add_email(email, primary=True)

        if verbosity >= 1:
            self.stdout.write("Superuser created successfully.\n")
