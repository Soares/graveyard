from datetime import datetime
from django.contrib.auth.backends import ModelBackend
from activator.models import User

class TokenBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, type, token):
        try:
            record = type.objects.get(token=token)
        except type.DoesNotExist:
            return None
        if record.expires < datetime.now():
            return None
        if record.used:
            return None
        return record.user
