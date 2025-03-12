from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class PlainTextPasswordBackend(ModelBackend):
    """
    Custom authentication backend to handle plaintext passwords.
    This is INSECURE and should only be used temporarily while migrating passwords.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if user.password == password:  # Direct plaintext comparison
                return user
        except User.DoesNotExist:
            return None