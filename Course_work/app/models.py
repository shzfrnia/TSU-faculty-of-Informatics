from hashlib import md5
from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.sql.expression import func
import json
from app import db, lm

ROLE_USER = 0
ROLE_ADMIN = 1
NON_PUBLIC = 0
PUBLIC = 1


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(60), index=True,
                      unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    about_me = db.Column(db.String(140))
    admin = db.Column(db.SmallInteger, default=ROLE_USER, nullable=False)

    def get_id(self):
        return str(self.user_id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_notepads(self):
        notepads = self.get_notepads().all()
        notepads_for_test = []
        for n in notepads:
            dif = (datetime.now().date() - n.day_when_learned).days
            if dif >= n.day_to_repeat:
                notepads_for_test.append(n)
        return notepads_for_test

    def create_notepad(self, name, description="", subject="", public=NON_PUBLIC):
        params = {
            "name": name,
            "description": description,
            "subject": subject,
            "public": public,
            "user_user_id": self.user_id,
            "day_when_learned": None
        }
        new_notepad = Notepad(**params)
        return new_notepad

    def get_notepad(self, notepad_id):
        notepad_query = Notepad.query.filter_by(notepad_id=notepad_id)
        notepad = notepad_query.first_or_404()
        notepad_is_public = notepad.is_public()
        user_is_owner = self.is_owner(notepad)
        if not user_is_owner and not notepad_is_public:
            return None
        else:
            return notepad_query

    def change_login(self, new_login):
        self.login = new_login

    def set_about_me(self, new_about_me):
        self.about_me = new_about_me

    def delete_notepad(self, notepad):
        cards = notepad.first().get_cards()
        notepad.delete()
        cards.delete()

    def get_notepads(self):
        return Notepad.query.filter(Notepad.user_user_id == self.user_id)

    def is_owner(self, notepad):
        return self.user_id == notepad.user_user_id

    def get_public_notepads(self):
        users_notepads = self.get_notepads()
        return users_notepads.filter(Notepad.public == PUBLIC)

    def avatar(self, size):
        digest = md5(self.login.lower().encode('utf-8')).hexdigest()
        # digest = md5('pugumo68@gmail.com'.lower().encode('utf-8')).hexdigest()
        return 'https://s.gravatar.com/avatar/{}?&d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User %r>' % (self.login)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)


class Notepad(db.Model):
    notepad_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(300))
    subject = db.Column(db.String(100), default="Other", nullable=False)
    public = db.Column(db.SmallInteger, default=NON_PUBLIC, nullable=False)
    day_to_repeat = db.Column(db.Integer, default=1, nullable=False)
    day_when_learned = db.Column(db.Date,default=datetime.now().date() , nullable=True)
    user_user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('name', 'user_user_id', name='names_uniq_constr'),
    )

    def __repr__(self):
        return '<Notepad %r /%r/ %r>' % (self.name, self.day_to_repeat, self.day_when_learned)

    def get_cards_count(self):
        return Card.query.filter(Card.notepad_notepad_id == self.notepad_id).count()

    def is_public(self):
        return self.public == PUBLIC

    def add_card(self, first_part, last_part):
        params = {
            "notepad_notepad_id": self.notepad_id,
            "first_part": first_part,
            "last_part": last_part,
            "reverse_raiting": 0,
            "raiting": 0,
            "card_type": 0,
            "known": False
        }

        new_card = Card(**params)
        db.session.add(new_card)

    def repead_through(self):
        dif = (datetime.now().date() - self.day_when_learned).days
        return self.day_to_repeat - dif

    def get_owner(self):
        return User.query.filter_by(user_id=self.user_user_id)

    def is_learned(self):
        user = self.get_owner().first()
        user_notepads_checked = user.check_notepads()
        return self not in user_notepads_checked

    def get_cards(self, random=False):
        if random:
            return self.__get_random_cards()
        else:
            return Card.query.filter_by(notepad_notepad_id=self.notepad_id)

    def __get_random_cards(self):
        return self.get_cards().order_by(func.random())

    def clear_cards(self):
        self.get_cards().delete()

    def deserialize(self, json_string):
        json_data = json.loads(json_string)
        self.name = json_data["notepad_name"]
        self.description = json_data["notepad_description"]
        self.subject = json_data["notepad_subject"]
        self.public = f'{0 if json_data["public"] == False else 1}'
        self.day_to_repeat = 1
        self.day_when_learned = datetime.now().date()
        self.clear_cards()
        for card in json_data["cards"]:
            self.add_card(card["first_part"], card["last_part"])

    def to_json(self):
        notepad = {
            'notepad_id': self.notepad_id,
            'notepad_name': self.name,
            'notepad_description': self.description,
            'notepad_subject': self.subject,
            'public': self.public,
            'cards': [{"card_id": i.card_id, "fisrt_part": i.first_part, "last_part": i.last_part} for i in self.get_cards()]
        }
        myJson = json.dumps(notepad)
        return myJson

    @staticmethod
    def get_public_notepads():
        return Notepad.query.filter_by(public=PUBLIC)

    @staticmethod
    # TODO тут нужно еще возвращать и свои приватные.
    # Это для поиска!!!
    def get_notepads_by_name(name):
        return Notepad.query.filter_by(name=name, public=PUBLIC).all()


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    first_part = db.Column(db.String(300), nullable=False)
    last_part = db.Column(db.String(300), nullable=False)

    # init types of card
    card_type = db.Column(db.Integer, nullable=False)

    known = db.Column(db.Boolean, default=True, nullable=False)
    raiting = db.Column(db.Float, default=0, nullable=False)
    reverse_raiting = db.Column(db.Float, default=0, nullable=False)
    notepad_notepad_id = db.Column(
        db.Integer, db.ForeignKey('notepad.notepad_id'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('notepad_notepad_id', 'first_part',
                            'last_part', name='cards_uniq_constr'),
    )

    def get_self_notepad(self):
        return Notepad.query.filter_by(notepad_id=self.notepad_notepad_id)

    def is_known(self):
        return self.known

    def __repr__(self):
        return '<Card %r>' % (self.first_part)
