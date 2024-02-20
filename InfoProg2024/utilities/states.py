from enum import Enum


class State(Enum):
    """
    A program megfelelő állapotai
    MENU - főmenu
    GAME - játék
    HIGH_SCORES - ranksor
    SETTINGS - beállítások
    HELLO_SCREEN - Indításkor felugró ablak, itt tudjuk megadni a nevünket
    """
    MENU = 1
    GAME = 2
    HIGH_SCORES = 3
    SETTINGS = 4
    HELLO_SCREEN = 5


class GameStates(Enum):
    """
    Játék állapotai:
    DICE_THROW - dobás folyamata
    SCORING - pontozás
    END_GAME - játék vége
    PLAYER_CHOOSE - mikor a játékos kiválasztja az általa kívánt pontozó ablakot
    WAITING - az állapotok közötti várakozó
    SAVING - mentés
    LOADING - betöltés
    """
    DICE_THROW = 1
    SCORING = 2
    END_GAME = 3
    PLAYER_CHOOSE = 4
    WAITING = 5
    SAVING = 6
    LOADING = 7
