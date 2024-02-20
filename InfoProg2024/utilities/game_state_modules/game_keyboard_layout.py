from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities import assets


def game_keyboard_layout(control: GUIController):
    """
    A játék felületen az animált gombokat irányítja
    """

    # Fel
    control.game_screen.blit(assets.tooltip_font.render("Fel", True, assets.FontColors.cream), (480, 500))
    if control.keyboard.UP_PRESSED:
        control.game_screen.blit(assets.keyboard_up_2, (430, 490))
    else:
        control.game_screen.blit(assets.keyboard_up_1, (430, 490))

    # Le
    control.game_screen.blit(assets.tooltip_font.render("Le", True, assets.FontColors.cream), (480, 530))
    if control.keyboard.DOWN_PRESSED:
        control.game_screen.blit(assets.keyboard_down_2, (430, 520))
    else:
        control.game_screen.blit(assets.keyboard_down_1, (430, 520))

    control.game_screen.blit(assets.tooltip_font.render("Érték megadása", True, assets.FontColors.cream), (500, 555))

    # Enter
    if control.keyboard.ENTER_PRESSED:
        control.game_screen.blit(assets.keyboard_enter_2, (540, 495))
    else:
        control.game_screen.blit(assets.keyboard_enter_1, (540, 495))

    control.game_screen.blit(assets.tooltip_font.render("Dobás/", True, assets.FontColors.cream), (250, 540))
    control.game_screen.blit(assets.tooltip_font.render("Következö kör", True, assets.FontColors.cream), (250, 555))

    # Space
    if control.keyboard.SPACE_PRESSED:
        control.game_screen.blit(assets.keyboard_space_2, (250, 500))
    else:
        control.game_screen.blit(assets.keyboard_space_1, (250, 500))

    control.game_screen.blit(assets.tooltip_font.render("Mentés", True, assets.FontColors.cream), (100, 510))
    if control.keyboard.S_PRESSED:
        control.game_screen.blit(assets.keyboard_s_2, (190,500))
    else:
        control.game_screen.blit(assets.keyboard_s_1, (190, 500))

