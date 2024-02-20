import pygame

from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities import assets
from InfoProg2024.utilities.states import State, GameStates
from InfoProg2024.utilities.game_state_modules.reset_game import reset_game
from InfoProg2024.utilities.loading import load_game

from InfoProg2024.utilities.settings.settings import SAVE_FILE_PATH
import os
import logging
def main_menu(control: GUIController) -> None:
    """
    Ez az eljárás foglalkozik a főmenüvel, a menüben megtalálható menüpontok:
        - Új játék
        - Folytatás
        - Ranklista
        - Beállítások
    """

    control.game_screen.blit(assets.main_menu_background_image, (0, 0))
    if os.path.isfile(SAVE_FILE_PATH):
        control.game_screen.blit(assets.continue_game, (550, 200))
    else:
        control.game_screen.blit(assets.no_continue_game, (550, 200))
    control.game_screen.blit(assets.new_game, (550, 280))
    control.game_screen.blit(assets.high_scores, (550, 360))
    control.game_screen.blit(assets.settings, (550, 440))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and not control.keyboard.DOWN_PRESSED:
                control.keyboard.DOWN_PRESSED = True
                if control.MENU_POINTER < 3:
                    control.MENU_POINTER += 1

            if event.key == pygame.K_UP and not control.keyboard.UP_PRESSED:
                control.keyboard.UP_PRESSED = True

                if control.MENU_POINTER > 0:
                    if control.MENU_POINTER > 1 or control.SAVE_GAME:
                        control.MENU_POINTER -= 1

            if event.key == pygame.K_RETURN and not control.keyboard.ENTER_PRESSED:
                match control.MENU_POINTER:
                    case 0:  # Folytatás
                        if os.path.isfile(SAVE_FILE_PATH):
                            control.STATE = State.GAME
                            control.SAVE_GAME = False

                            control.GAME_STATE = GameStates.LOADING
                            load_game(control)
                            control.GAME_STATE = GameStates.WAITING

                            try:
                                os.remove(SAVE_FILE_PATH)
                            except FileNotFoundError:
                                logging.warn("Nincs meg a keresett fajl")

                    case 1:  # Új játék
                        reset_game(control)
                        control.STATE = State.GAME
                        control.GAME_STATE = GameStates.WAITING

                    case 2:  # Ranklista
                        control.STATE = State.HIGH_SCORES
                    case 3:  # Beállítások
                        control.STATE = State.SETTINGS

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and control.keyboard.DOWN_PRESSED:
                control.keyboard.DOWN_PRESSED = False

            if event.key == pygame.K_UP and control.keyboard.UP_PRESSED:
                control.keyboard.UP_PRESSED = False

            if event.key == pygame.K_RETURN and control.keyboard.ENTER_PRESSED:
                control.keyboard.ENTER_PRESSED = False

    control.game_screen.blit(assets.menu_pointer_image, (480, 200 + 80 * control.MENU_POINTER))  # Menü mutató

    return
