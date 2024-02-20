from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities.states import GameStates


def reset_game(control: GUIController) -> None:
    """
    A játékot alapállapotba rakja, a játszma újraindításakor használatos
    """

    control.game_controller.reset()
    control.game_scoreboard.reset()

    control.GAME_STATE = GameStates.WAITING
