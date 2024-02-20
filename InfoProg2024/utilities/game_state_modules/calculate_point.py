from typing import List, Tuple, Callable

from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities.scoreboard import ScoreType
from InfoProg2024.utilities.states import GameStates


def calculate_point(control: GUIController) -> None:
    """
    Két állapot van:
    Játékos van soron - ekkor dobás után kiszámolja a lehetséges mezőkre a pontszámot
                        és kiírja egy oszlopba.
    CPU van soron - ekkor a gép a saját lépést kiírja az oszlopába
    """

    if control.game_controller.active.is_cpu and control.GAME_STATE == GameStates.SCORING:
        chosen: Tuple[int, Callable] = control.game_controller.active.play_hand()

        score: int = chosen[0]
        func: Callable = chosen[1]

        control.game_scoreboard.create_text(score, func, ScoreType.CPU_SCORE)
        control.game_controller.active.player_roll = False
        control.game_controller.active.maradek_jatek -= 1
        control.GAME_STATE = GameStates.WAITING
        control.game_controller.change_active_player()

        return
    else:
        control.GAME_STATE = GameStates.PLAYER_CHOOSE

        pontok: List[Tuple[int, Callable]] = control.game_controller.active.ertekelesek_futtatasa()



        for p, func in pontok:
            control.game_scoreboard.create_text(p, func, ScoreType.CALCULATED_SCORE)
