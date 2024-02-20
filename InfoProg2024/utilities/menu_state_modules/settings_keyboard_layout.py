from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities import assets


def settings_keyboard_layout(control: GUIController):
    """
    A játék felületen az animált gombokat irányítja
    """

    # Fel
    control.game_screen.blit(assets.tooltip_font.render("Fel", True, assets.FontColors.cream), (570, 430))
    if control.keyboard.UP_PRESSED:
        control.game_screen.blit(assets.keyboard_up_2, (620, 420))
    else:
        control.game_screen.blit(assets.keyboard_up_1, (620, 420))

    # Le
    control.game_screen.blit(assets.tooltip_font.render("Le", True, assets.FontColors.cream), (570, 460))
    if control.keyboard.DOWN_PRESSED:
        control.game_screen.blit(assets.keyboard_down_2, (620, 450))
    else:
        control.game_screen.blit(assets.keyboard_down_1, (620, 450))

    control.game_screen.blit(assets.tooltip_font.render("Ki/Be kapcsolás", True, assets.FontColors.cream), (680, 490))
    control.game_screen.blit(assets.tooltip_font.render("Névváltoztatás", True, assets.FontColors.cream), (680, 510))

    # Enter
    if control.keyboard.ENTER_PRESSED:
        control.game_screen.blit(assets.keyboard_enter_2, (750, 420))
    else:
        control.game_screen.blit(assets.keyboard_enter_1, (750, 420))
