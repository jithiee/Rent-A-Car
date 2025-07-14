from django.contrib.auth.backends import ModelBackend
from .models import Account

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Account.objects.get(email=email)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None
