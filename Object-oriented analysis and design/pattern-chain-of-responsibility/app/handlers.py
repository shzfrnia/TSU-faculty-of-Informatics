from app.handler import TranslateHandler


class TranslatorRusEn(TranslateHandler):
    def __init__(self):
        self._from_language = 'ru'
        self._to_language = 'en'

    def _can_translate(self, text, to_language):
        return super()._can_translate(text, to_language)


class TranslatorRusUk(TranslateHandler):
    def __init__(self):
        self._from_language = 'ru'
        self._to_language = 'uk'

    def _can_translate(self, text, to_language):
        return super()._can_translate(text, to_language)


class TranslateEnRus(TranslateHandler):
    def __init__(self):
        self._from_language = 'en'
        self._to_language = 'ru'

    def _can_translate(self, text, to_language):
        return super()._can_translate(text, to_language)


class TranslateEnUk(TranslateHandler):
    def __init__(self):
        self._from_language = 'en'
        self._to_language = 'uk'

    def _can_translate(self, text, to_language):
        return super()._can_translate(text, to_language)


class TerminateHandler(TranslateHandler):
    def __init__(self):
        self._from_language = None
        self._to_language = None

    def _can_translate(self, text, to_language):
        return super()._can_translate(text, to_language)

    def translate(self, text, to_language):
        return None
