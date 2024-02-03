from enum import Enum


class State(Enum):
    MENU = 1
    GAME = 2
    HIGH_SCORES = 3
    SETTINGS = 4

class GameStates(Enum):
    DICE_THROW = 1
    SCORING = 2
    END_GAME = 3
    PLAYER_CHOOSE = 4
    WAITING = 5
    SAVING = 6
    LOADING = 7
