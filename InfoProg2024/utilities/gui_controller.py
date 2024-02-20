from InfoProg2024.utilities.states import GameStates, State
from InfoProg2024.utilities.keyboard_press import Keyboard

from datetime import timedelta

class GUIController:
    """
    Kapcsolatot alakít ki a játék logikája, a ponttábla(scoreboard) és a képernyő (screen) között.

    :param screen - képernyő objektum - pygame.display
    :param game_controller - játék vezérlő objektum
    :param game_scoreboard - pontozó tábla
    """
    def __init__(self, screen, game_controller, game_scoreboard):

        # Fő játék irányításához szükséges változók
        self.INDEX = 0
        self.SAVE_GAME = True
        self.MENU_POINTER = 1
        self.MENU_SETTINGS_POINTER = 0
        self.IS_NAME_CHANGING = False
        self.NAME_USER_TEXT = ""
        self.HELLO_SCREEN_POINTER = 0
        self.DIFFICULTY_INDEX = 0

        self.IS_SAVING_TEXT = False
        self.IS_SAVING_TEXT_START_TIME = None
        self.IS_SAVING_TEXT_DELTA = timedelta(seconds=3)

        self.STATE = State.HELLO_SCREEN
        self.GAME_STATE = GameStates.WAITING


        self.keyboard = Keyboard() # A billentyű lenyomását érzékeli

        self.game_screen = screen
        self.game_controller = game_controller
        self.game_scoreboard = game_scoreboard

        self.MAX_NAME_LENGTH = 20
