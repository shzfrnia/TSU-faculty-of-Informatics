from app.models import User


class UserSpecialCase(User):
    """It is Special Case pattern for User object
    Note:
        Always using query object from SQLAlchemy it's reason for first() function which returns self.
    """

    def __init__(self):
        self.login = "UserSpecialCaseName!"

    def is_active(self):
        return False

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return False

    def check_password(self, password):
        return False

    def first(self):
        return self