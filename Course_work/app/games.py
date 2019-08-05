from app.game import Game
from app.flashProxy import FlashProxy
from flask import url_for
from flask import render_template
from flask import redirect
from datetime import datetime
from app import db

CLASSIC_GAME = 0
NON_CLASSIC_GAME = 1


class ClassicGame(Game):
    def __init__(self, notepad):
        self._name = "Classic"
        self._notepad = notepad

    def get_mode_id(self):
        return CLASSIC_GAME

    def run(self):
        random_card = self._notepad.get_cards(
            random=True).filter_by(known=False).first()

        if random_card is None:
            self._notepad.day_to_repeat += self._notepad.day_to_repeat
            self._notepad.day_when_learned = datetime.now().date()
            db.session.commit()
            FlashProxy.flash(
                "You have learned all cards in this notepad.", FlashProxy.SUCCESS)
            return redirect(url_for('preview_notepad', notepad_id=self._notepad.notepad_id))

        notepad_cards_known = self._notepad.get_cards().filter_by(known=True).count()
        notepad_cards_all = self._notepad.get_cards_count()
        procent = int(notepad_cards_known/notepad_cards_all * 100)
        return render_template("playgrounds/learn_classic.html",
                               title='Classic mode',
                               notepad=self._notepad,
                               play_mode=self.get_mode_id(),
                               card=random_card,
                               procent=procent)


class NonClassicGame(Game):
    def __init__(self, notepad):
        self._name = "NonClassic"
        self._notepad = notepad

    def get_mode_id(self):
        return NON_CLASSIC_GAME

    def run(self):
        return render_template("playgrounds/learn_non_classic.html",
                               title='Non Classic mode',
                               notepad=self._notepad)
