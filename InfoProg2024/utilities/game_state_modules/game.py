import pygame
import logging

from InfoProg2024.utilities.states import GameStates

from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities import assets

from InfoProg2024.utilities.game_state_modules.end_game import end_game
from InfoProg2024.utilities.game_state_modules.waiting import waiting
from InfoProg2024.utilities.game_state_modules.render_dices import render_dices
from InfoProg2024.utilities.game_state_modules.throw_state import throw_state
from InfoProg2024.utilities.game_state_modules.game_keyboard_layout import game_keyboard_layout
from InfoProg2024.utilities.saving import save_game
from InfoProg2024.utilities.loading import load_game
from InfoProg2024.utilities.scoreboard import ScoreType

from InfoProg2024.utilities.settings import settings
from datetime import datetime


def game(control: GUIController):
    """
    A játék állapotot foglalja magában, megvannak a saját állapotai GameStates
    GameStates:
            1 - DICE_THROW - Dobás állapota
            2 - SCORING - Pontozás állapota
            3 - END_GAME - Játék vége
            4 - PLAYER_CHOOSE - A kockák pontozása után a játékos kiválasztja a megfelelő helyet, ahova beírja a pontot
            5 - WAITING - várakozás bemenetre
            6 - SAVING - mentés folyamatban
            7 - LOADING - betöltés folyamatban

    Ezen felül a játék irányítása is itt található
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not control.keyboard.UP_PRESSED:

                control.keyboard.UP_PRESSED = True

                if control.INDEX > 0:
                    control.INDEX -= 1
                    assets.highlight_image_rectangle.y -= assets.HIGLIGHT_DELTA

            if event.key == pygame.K_RIGHT and control.GAME_STATE == GameStates.WAITING:
                control.GAME_STATE = GameStates.LOADING
                load_game(control)
                control.GAME_STATE = GameStates.WAITING

                logging.info("Játék betöltve")

            if event.key == pygame.K_DOWN and not control.keyboard.DOWN_PRESSED:
                control.keyboard.DOWN_PRESSED = True

                if control.INDEX < settings.KOMBO_SZAM - 1:
                    control.INDEX += 1
                    assets.highlight_image_rectangle.y += assets.HIGLIGHT_DELTA

            if event.key == pygame.K_SPACE and not control.keyboard.SPACE_PRESSED:
                control.keyboard.SPACE_PRESSED = True

            if event.key == pygame.K_s and not control.keyboard.S_PRESSED and control.GAME_STATE.value == GameStates.WAITING.value:
                control.GAME_STATE = GameStates.SAVING

                control.IS_SAVING_TEXT = True
                control.IS_SAVING_TEXT_START_TIME = datetime.now()

                save_game(control.game_controller, control.game_scoreboard)
                control.GAME_STATE = GameStates.WAITING

                logging.info("Játék elmentve")

                control.keyboard.S_PRESSED = True

            if event.key == pygame.K_RETURN and not control.keyboard.ENTER_PRESSED and not control.game_controller.active.is_cpu:
                control.keyboard.ENTER_PRESSED = True

                if control.GAME_STATE == GameStates.PLAYER_CHOOSE:
                    # Kiválasztjuk az INDEXet, ha nincs ott még semmi beírva, akkor az adott értéket oda írjuk be

                    valasztott_kombinacio: Callable = control.game_controller.active.kombinaciok[control.INDEX]

                    if control.game_scoreboard.player_scores[valasztott_kombinacio] is None:
                        control.game_scoreboard.create_text(
                            score=control.game_controller.active.kiszamolt_pontok[valasztott_kombinacio],
                            func=valasztott_kombinacio,
                            score_type=ScoreType.PLAYER_SCORE)
                        control.game_controller.active.maradek_jatek -= 1

                        control.game_controller.change_active_player()
                        control.GAME_STATE = GameStates.WAITING

                        for key in control.game_scoreboard.player_calculated_scores.keys():
                            control.game_scoreboard.player_calculated_scores[key] = None

                        return
                    else:
                        logging.debug("A pontozó mező használatban van")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and control.keyboard.UP_PRESSED:
                control.keyboard.UP_PRESSED = False

            if event.key == pygame.K_DOWN and control.keyboard.DOWN_PRESSED:
                control.keyboard.DOWN_PRESSED = False

            if event.key == pygame.K_s and control.keyboard.S_PRESSED:
                control.keyboard.S_PRESSED = False

            if event.key == pygame.K_SPACE and control.keyboard.SPACE_PRESSED:
                control.keyboard.SPACE_PRESSED = False

            if event.key == pygame.K_RETURN and control.keyboard.ENTER_PRESSED:
                control.keyboard.ENTER_PRESSED = False

    control.game_screen.blit(assets.background_image, (0, 0))  # háttér

    control.game_screen.blit(assets.highlight_image, assets.highlight_image_rectangle)  # kijelőlő téglalap

    if control.game_controller.active.maradek_jatek + control.game_controller.inactive.maradek_jatek <= 0:
        control.GAME_STATE = GameStates.END_GAME

    match control.GAME_STATE:
        case GameStates.DICE_THROW:
            throw_state(control)
        case GameStates.PLAYER_CHOOSE:
            render_dices(control)
        case GameStates.WAITING:
            waiting(control)
            render_dices(control)
        case GameStates.END_GAME:
            end_game(control)
            return

    if control.game_controller.player_turn:  # Rámutat arra a kocka sorra, amelyik éppen soron van
        control.game_screen.blit(assets.turn_pointer, (625, 390))
    else:
        control.game_screen.blit(assets.turn_pointer, (625, 125))

    game_keyboard_layout(control)
    control.game_scoreboard.draw_scoreboard()

    if control.IS_SAVING_TEXT:
        if datetime.now() < control.IS_SAVING_TEXT_START_TIME + control.IS_SAVING_TEXT_DELTA:
            control.game_screen.blit(assets.tooltip_font.render("Mentés...", True, assets.FontColors.yellow), (110, 550))
            print("MENT::S")
        else:
            control.IS_SAVING_TEXT = False
            control.IS_SAVING_TEXT_START_TIME = None
