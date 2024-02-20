from InfoProg2024.utilities.gui_controller import GUIController


def render_dices(control: GUIController) -> None:
    """
    Rendereli a kockákat alap állapotukban
    """
    for d in control.game_controller.active.dice_entities:
        control.game_screen.blit(d.value_image, (d.x, d.y))
    for d in control.game_controller.inactive.dice_entities:
        control.game_screen.blit(d.value_image, (d.x, d.y))
