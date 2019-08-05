from app import db
from app.models import User, Notepad, Card
from app.specialcases import UserSpecialCase


class UserTableGateway():
    @staticmethod
    def login_is_exists(login):
        """
        Returns:
            bool: True if login exists in database.
        """
        return User.query.filter_by(login=login).first() != None

    @staticmethod
    def get_user_by_login(login):
        """
        Returns:
            query: The query object.
        """
        user_query = User.query.filter_by(login=login)
        user = user_query.first()
        if user is None:
            return UserSpecialCase()
        else:
            return user_query


class CardTableGateway():
    @staticmethod
    def get_card_by_id(card_id):
        """
        Returns:
            query: The query object.
        """
        return Card.query.filter_by(card_id=card_id)
