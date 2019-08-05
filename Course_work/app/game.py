from flask import url_for
from abc import ABC, abstractmethod, abstractstaticmethod


class Game(ABC):
    def __init__(self, notepad):
        self._name = None
        self._description = "Let's play"
        self._mode = None
        self._link = url_for(
            'learn', notepad_id=notepad.notepad_id, mode=self._mode)
        self._notepad = notepad

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def link(self):
        return self._link

    @abstractmethod
    def run(self):
        raise NotImplementedError("This method can be implement")

    @abstractstaticmethod
    def get_mode_id(self):
        raise NotImplementedError("Each of games must have id")
