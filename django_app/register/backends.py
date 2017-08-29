from django.contrib.auth import get_user_model

User = get_user_model()


class EmailAuthBackend:

    def authenticate(self, email="", password=""):
        try:
            user = User.objects.get(email=email)
            if user.check_password(str(password)):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
