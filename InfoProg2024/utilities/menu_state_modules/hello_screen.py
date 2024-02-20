import pygame

from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities import assets
from InfoProg2024.utilities.states import State


def hello_screen(control: GUIController) -> None:
    """
    Beállításuk menüpont, itt található beállítások:
        - Nehézség - HARDMODE, vagy EASYMODE
        - Név - Enter lenyomásával átírható
    """
    control.game_screen.blit(assets.hello_screen_image, (0, 0))
    control.game_screen.blit(assets.highlight_image, (430, 295))
    control.game_screen.blit(
            assets.highscore_menu_font.render(str(control.NAME_USER_TEXT), True, assets.FontColors.cream),
            (450, 300))
    # Beállítások kiírása

    control.game_screen.blit(assets.menu_pointer_image, (390, 300 + 80 * control.HELLO_SCREEN_POINTER))

    control.game_screen.blit(assets.highscore_font.render(f"Adj meg egy nevet (max. 20):", True, assets.FontColors.cream), (430, 265))

    if control.DIFFICULTY_INDEX == 0:
        assets.TextBox(control.game_screen, "EASY", 530, 400, assets.highscore_menu_font,assets.text_box_2).render()
        control.game_screen.blit(
            assets.highscore_menu_font.render(f"HARD", True, assets.FontColors.cream), (675, 382))
    else:
        control.game_screen.blit(
            assets.highscore_menu_font.render(f"EASY", True, assets.FontColors.cream), (495, 382))
        assets.TextBox(control.game_screen, "HARD", 710, 400, assets.highscore_menu_font,assets.text_box_2).render()

    for event in pygame.event.get():

        """
        Név változás folyamat, figyeli mely betűket nyomunk le, lehetséges a törlés is
        """
        if event.type == pygame.KEYDOWN:
            match control.HELLO_SCREEN_POINTER:
                case 0:
                    if event.key == pygame.K_BACKSPACE:
                        control.NAME_USER_TEXT = control.NAME_USER_TEXT[:-1]

                    elif event.key == pygame.K_RETURN and control.NAME_USER_TEXT.strip() != "":
                        control.game_controller.player_name = control.NAME_USER_TEXT
                        control.HELLO_SCREEN_POINTER = 1
                        #control.STATE = State.MENU

                    else:
                        if not (control.NAME_USER_TEXT.strip() == "" and event.unicode == " "):
                            if len(control.NAME_USER_TEXT) <= control.MAX_NAME_LENGTH:
                                control.NAME_USER_TEXT += event.unicode

                case 1:

                    if event.key == pygame.K_LEFT and not control.keyboard.LEFT_PRESSED:
                        if control.DIFFICULTY_INDEX != 0:
                            control.DIFFICULTY_INDEX -= 1

                    if event.key == pygame.K_RIGHT and not control.keyboard.RIGHT_PRESSED:
                        if control.DIFFICULTY_INDEX != 1:
                            control.DIFFICULTY_INDEX += 1

                    if event.key == pygame.K_RETURN and not control.keyboard.ENTER_PRESSED:

                        if control.DIFFICULTY_INDEX == 0:
                            control.game_controller.cpu.set_easy_mode()
                        else:
                            control.game_controller.cpu.set_hard_mode()

                        control.STATE = State.MENU


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

                    match control.MENU_SETTINGS_POINTER:
                        case 0:  # HARDMODE
                            print("this")
                            #if control.game_controller.cpu.hard_mode:
                            #    control.game_controller.cpu.set_easydasd
                            #    control.game_controller.cpu.set_hard_mode()

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
