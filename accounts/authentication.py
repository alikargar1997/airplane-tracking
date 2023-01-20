from .models import CustomUser as User


class EmailAuthentication:
    """Authenticate user by email"""

    def authenticate(self, username: str = None, password: str = None) -> User:
        user = User.objects.get_by_email(email=username)
        if user and user.check_password(password):
            return user
        else:
            return None

    def get_user(self, user_id: int) -> User:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
