from django.contrib.auth.backends import ModelBackend
from authenticator.models import User

class LocalBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, email, password):
        try:
            user = User.objects.with_email(email)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
