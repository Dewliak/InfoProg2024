import pygame

from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities import assets
from InfoProg2024.utilities.states import State
from InfoProg2024.utilities.menu_state_modules.settings_keyboard_layout import settings_keyboard_layout

def settings_screen(control: GUIController) -> None:
    """
    Beállításuk menüpont, itt található beállítások:
        - Nehézség - HARDMODE, vagy EASYMODE
        - Név - Enter lenyomásával átírható
    """

    control.game_screen.blit(assets.settings_image, (0, 0))

    if control.IS_NAME_CHANGING:  # Név váltás

        control.game_screen.blit(assets.highlight_image, (430, 295))
        control.game_screen.blit(
            assets.highscore_menu_font.render(str(control.NAME_USER_TEXT), True, assets.FontColors.cream),
            (545, 300))
    else:
        control.game_screen.blit(
            assets.highscore_menu_font.render(str(control.game_controller.player_name), True, assets.FontColors.cream),
            (545, 300))

    # Beállítások kiírása

    control.game_screen.blit(assets.menu_pointer_image, (400, 200 + 100 * control.MENU_SETTINGS_POINTER))

    control.game_screen.blit(assets.highscore_menu_font.render(f"Name:", True, assets.FontColors.cream), (440, 300))

    control.game_screen.blit(assets.highscore_menu_font.render("Hardmode", True, assets.FontColors.cream), (440, 200))
    control.game_screen.blit(assets.settings_check_box, (750, 195))

    if control.game_controller.cpu.hard_mode:
        control.game_screen.blit(assets.settings_check, (750, 195))

    for event in pygame.event.get():

        if control.IS_NAME_CHANGING:
            """
            Név változás folyamat, figyeli mely betűket nyomunk le, lehetséges a törlés is
            """
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    control.NAME_USER_TEXT = control.NAME_USER_TEXT[:-1]

                elif event.key == pygame.K_RETURN and control.NAME_USER_TEXT.strip() != "":
                    control.IS_NAME_CHANGING = False
                    control.game_controller.player_name = control.NAME_USER_TEXT

                else:
                    if not (control.NAME_USER_TEXT.strip() == "" and event.unicode == " "):
                        if len(control.NAME_USER_TEXT) <= control.MAX_NAME_LENGTH:
                            control.NAME_USER_TEXT += event.unicode
        else:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and not control.keyboard.DOWN_PRESSED:
                    control.keyboard.DOWN_PRESSED = True
                    if control.MENU_SETTINGS_POINTER < 1:
                        control.MENU_SETTINGS_POINTER += 1

                if event.key == pygame.K_UP and not control.keyboard.UP_PRESSED:
                    control.keyboard.UP_PRESSED = True

                    if control.MENU_SETTINGS_POINTER > 0:
                        control.MENU_SETTINGS_POINTER -= 1

                if event.key == pygame.K_RETURN and not control.keyboard.ENTER_PRESSED:
                    control.keyboard.ENTER_PRESSED = True
                    match control.MENU_SETTINGS_POINTER:
                        case 0:  # HARDMODE

                            if control.game_controller.cpu.hard_mode:
                                control.game_controller.cpu.set_easy_mode()
                            else:
                                control.game_controller.cpu.set_hard_mode()

                        case 1:  # Név változtatás
                            if not control.IS_NAME_CHANGING:
                                control.IS_NAME_CHANGING = True
                            control.NAME_USER_TEXT = ""
                            control.game_controller.player_name = control.NAME_USER_TEXT

                if event.key == pygame.K_BACKSPACE and not control.keyboard.BACKSPACE_PRESSED:
                    control.keyboard.BACKSPACE_PRESSED = True
                    control.STATE = State.MENU

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN and control.keyboard.DOWN_PRESSED:
                    control.keyboard.DOWN_PRESSED = False

                if event.key == pygame.K_UP and control.keyboard.UP_PRESSED:
                    control.keyboard.UP_PRESSED = False

                if event.key == pygame.K_RETURN and control.keyboard.ENTER_PRESSED:
                    control.keyboard.ENTER_PRESSED = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE and control.keyboard.BACKSPACE_PRESSED:
                        control.keyboard.BACKSPACE_PRESSED = False

    settings_keyboard_layout(control)