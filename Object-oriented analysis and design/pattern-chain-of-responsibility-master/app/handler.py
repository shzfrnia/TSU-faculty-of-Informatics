from googletrans import Translator
from abc import ABC, abstractmethod


class TranslateHandler(ABC):
    def __init__(self):
        self._successor = None
        self._from_language = None
        self._to_language = None

    def set_next(self, next_handler):
        self._successor = next_handler
        return self

    @abstractmethod
    def _can_translate(self, text, to_language):
        translator = Translator()
        text_language = translator.detect(text).lang
        return (self._from_language == text_language and self._to_language == to_language)

    def translate(self, text, to_language):
        translator = Translator()
        if self._can_translate(text, to_language):
            return translator.translate(text, src=self._from_language, dest=self._to_language).text
        elif self._successor is not None:
            return self._successor.translate(text, to_language)
        else:
            raise ValueError("Nobody can handle it!")
