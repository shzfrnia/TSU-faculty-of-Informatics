from app.games import ClassicGame, NonClassicGame, CLASSIC_GAME, NON_CLASSIC_GAME
from flask import abort


class GameBulder():
    @staticmethod
    def build_game(game_mode, notepad):
        if game_mode == CLASSIC_GAME:
            return ClassicGame(notepad)
        elif game_mode == NON_CLASSIC_GAME:
            return NonClassicGame(notepad)
        else:
            abort(404)
