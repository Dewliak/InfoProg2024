import pygame
from sys import exit
from typing import Tuple, Callable, List

from InfoProg2024.modulok.player import controller, Controller

from utilities.keyboard_press import Keyboard
from utilities.states import State, GameStates
from utilities import game_initialization
from utilities.saving import save_game
from utilities.loading import load_game
from utilities.high_score import save_high_scores, load_high_scores, add_score_to_high_scores
from utilities.settings import settings

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

pygame.init()
clock = pygame.time.Clock()
game_screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Kockapóker")

from utilities import assets
from utilities.scoreboard import ScoreBoard, ScoreType

PLAYER_dices, CPU_dices = game_initialization.init_dices()

dices = PLAYER_dices + CPU_dices

# Fő változók inicializálása
scoreboard = ScoreBoard(game_screen)

controller.player.dice_entities = PLAYER_dices
controller.cpu.dice_entities = CPU_dices
controller.cpu.set_hard_mode()


class GUIController:
    def __init__(self, screen, game_controller, game_scoreboard):
        self.INDEX = 0
        self.SAVE_GAME = True
        self.MENU_POINTER = 1
        self.MENU_SETTINGS_POINTER = 0
        self.IS_NAME_CHANGING = False
        self.NAME_USER_TEXT = ""

        self.STATE = State.MENU
        self.GAME_STATE = GameStates.WAITING  # GameStates.WAITING

        self.keyboard = Keyboard()

        self.game_screen = screen
        self.game_controller = game_controller
        self.game_scoreboard = game_scoreboard


gui_controller = GUIController(game_screen, controller, scoreboard)


def game_keyboard_layout(control: gui_controller):
    """
    A játék felületen az animált gombokat irányítja
    """

    screen = gui_controller.game_screen

    # Fel
    screen.blit(assets.tooltip_font.render("Fel", True, assets.FontColors.cream), (480, 500))
    if control.keyboard.UP_PRESSED:
        screen.blit(assets.keyboard_up_2, (430, 490))
    else:
        screen.blit(assets.keyboard_up_1, (430, 490))

    # Le
    screen.blit(assets.tooltip_font.render("Le", True, assets.FontColors.cream), (480, 530))
    if control.keyboard.DOWN_PRESSED:
        screen.blit(assets.keyboard_down_2, (430, 520))
    else:
        screen.blit(assets.keyboard_down_1, (430, 520))

    screen.blit(assets.tooltip_font.render("Érték megadása", True, assets.FontColors.cream), (500, 555))

    # Enter
    if control.keyboard.ENTER_PRESSED:
        screen.blit(assets.keyboard_enter_2, (540, 495))
    else:
        screen.blit(assets.keyboard_enter_1, (540, 495))

    screen.blit(assets.tooltip_font.render("Dobás/", True, assets.FontColors.cream), (250, 540))
    screen.blit(assets.tooltip_font.render("Következö kör", True, assets.FontColors.cream), (250, 555))

    # Space
    if control.keyboard.SPACE_PRESSED:
        screen.blit(assets.keyboard_space_2, (250, 500))
    else:
        screen.blit(assets.keyboard_space_1, (250, 500))


def reset_game(control: GUIController) -> None:
    """
    A játékot alapállapotba rakja, a játszma újraindításakor használatos
    """

    control.game_controller.reset()
    control.game_scoreboard.reset()

    control.GAME_STATE = GameStates.WAITING


def end_game(control: GUIController) -> None:
    """
    A játszma befejező állapota. Ebben a részben van a pontok kiértékelése, győztes kinyilvánítása és
    a rekordok újraírása, ha szükséges. Az R betűt megnyomva újraindul a játék
    """
    key = pygame.key.get_pressed()

    if key[pygame.K_r]:
        reset_game(control)
        return

    high_scores = load_high_scores()

    control.game_screen.blit(assets.high_scores_image, (0, 0))  # háttér

    # Mivel ez az állapot egy loopban fut le csak első lefutáskor akarunk menteni
    if not control.game_controller.high_score_save:
        if scoreboard.player_score > scoreboard.cpu_score:
            logging.info("A játékos nyert")
            high_scores = add_score_to_high_scores(high_scores, scoreboard.player_score,
                                                   control.game_controller.player_name)
        else:
            logging.info("A CPU nyert")
            high_scores = add_score_to_high_scores(high_scores, scoreboard.cpu_score, "CPU")

        save_high_scores(high_scores)

        control.game_controller.high_score_save = True

    if scoreboard.player_score > scoreboard.cpu_score:
        control.game_screen.blit(assets.endgame_font.render("Nyertél", True, assets.FontColors.cream),
                                 (300, 100))  # TODO: set to gold
    else:
        control.game_screen.blit(assets.endgame_font.render("Vesztettél", True, assets.FontColors.cream),
                                 (300, 100))  # TODO: set to gold

    x = 910  # Ranksor koordináták
    y = 80
    delta = 50

    for i in range(10):
        rank = high_scores[i].rank
        name = high_scores[i].name
        score = high_scores[i].score
        text = f"{rank}, {name} - {score}"

        if i % 2 == 0:
            assets.TextBox(control.game_screen, f"{text: ^30}", x, y + i * delta, assets.highscore_font,
                           assets.score_board_box_1).render()
        else:
            assets.TextBox(control.game_screen, f"{text: ^30}", x, y + i * delta, assets.highscore_font,
                           assets.score_board_box_2).render()

    if scoreboard.player_score > scoreboard.cpu_score:
        control.game_screen.blit(
            assets.font.render(f"{control.game_controller.player_name} - {scoreboard.player_score} pont", True,
                               assets.FontColors.cream), (150, 250))
        control.game_screen.blit(
            assets.font.render(f"CPU - {scoreboard.cpu_score} pont", True, assets.FontColors.cream),
            (150, 320))
    else:
        control.game_screen.blit(
            assets.font.render(f"CPU - {scoreboard.cpu_score} pont", True, assets.FontColors.cream),
            (150, 250))
        control.game_screen.blit(
            assets.font.render(f"{control.game_controller.player_name} - {scoreboard.player_score} pont", True,
                               assets.FontColors.cream), (150, 320))

    control.game_screen.blit(assets.restart_font.render("Az újra indításhoz nyomj R-t", True, assets.FontColors.cream),
                             (180, 450))


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


def waiting(control: GUIController):
    """
    Dobások és értékelések közötti állapot. Vizsgálja, mikor indítjuk el a dobást
    """

    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        control.GAME_STATE = GameStates.DICE_THROW


def throw_state(control: GUIController):
    """
    Dobás állapota, szimulálja a dobásokat és lefut a dobás animáció
    """
    for d in control.game_controller.inactive.dice_entities:
        control.game_screen.blit(d.value_image, (d.x, d.y))

    if control.GAME_STATE == GameStates.DICE_THROW and control.game_controller.active.player_roll is False:
        # a player_roll az vizsgálja, hogy el vannak-e dobva a kockák

        control.game_controller.active.uj_dobas()

        assets.rolling_aud.play()

        control.game_controller.active.player_roll = True

        for i, d in enumerate(control.game_controller.active.dice_entities):
            control.game_controller.active.dice_entities[i].is_rolling = True

            control.game_controller.active.dice_entities[i].set_dice_value(
                control.game_controller.active.dobas.get_next())

            control.game_controller.active.dice_entities[i].set_image()

            # Dobás animáció
            control.game_screen.blit(control.game_controller.active.dice_entities[i].rolling_animation_image(),
                                     (d.x, d.y))
            control.game_controller.active.dice_entities[i].rolling_images_counter += 1

    else:
        if control.game_controller.active.player_roll:

            for i, d in enumerate(control.game_controller.active.dice_entities):

                if not d.is_rolling:
                    control.game_screen.blit(d.value_image, (d.x, d.y))  # rendereli a kockákat
                    continue

                control.game_screen.blit(control.game_controller.active.dice_entities[i].rolling_animation_image(),
                                         (d.x, d.y))

                control.game_controller.active.dice_entities[i].rolling_images_counter += 1

                if d.rolling_images_counter >= d.rolling_images_limit:
                    control.game_controller.active.dice_entities[i].is_rolling = False
                    control.game_controller.active.dice_entities[i].rolling_images_counter = 0

                    assets.rolling_stop_aud.play()

            if all(not x.is_rolling for x in
                   control.game_controller.active.dice_entities):  # ha már az egyik kocka sem pereg
                control.GAME_STATE = GameStates.SCORING

                calculate_point(control)

                control.game_controller.active.player_roll = False
        else:
            for d in control.game_controller.active.dice_entities:
                control.game_screen.blit(d.value_image, (d.x, d.y))

        if not control.game_controller.active.player_roll:  # ha nem pörögnek a kockák, akkor csak a kockákat renderelje
            for d in control.game_controller.active.dice_entities:
                control.game_screen.blit(d.value_image, (d.x, d.y))


def render_dices(control: GUIController) -> None:
    """
    Rendereli a kockákat alap állapotukban
    """
    for d in control.game_controller.active.dice_entities:
        control.game_screen.blit(d.value_image, (d.x, d.y))
    for d in control.game_controller.inactive.dice_entities:
        control.game_screen.blit(d.value_image, (d.x, d.y))


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

            if event.key == pygame.K_LEFT and control.GAME_STATE == GameStates.WAITING:
                control.GAME_STATE = GameStates.SAVING
                save_game(control.game_screen, control.game_scoreboard)
                control.GAME_STATE = GameStates.WAITING

                logging.info("Játék elmentve")

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

            if event.key == pygame.K_RETURN and not control.keyboard.ENTER_PRESSED and not control.game_controller.active.is_cpu:
                control.keyboard.ENTER_PRESSED = True

                if control.GAME_STATE == GameStates.PLAYER_CHOOSE:
                    # Kiválasztjuk az INDEXet, ha nincs ott még semmi beírva, akkor az adott értéket oda írjuk be

                    valasztott_kombinacio: Callable = control.game_controller.active.kombinaciok[control.INDEX]

                    if scoreboard.player_scores[valasztott_kombinacio] is None:

                        scoreboard.create_text(
                            score=control.game_controller.active.kiszamolt_pontok[valasztott_kombinacio],
                            func=valasztott_kombinacio,
                            score_type=ScoreType.PLAYER_SCORE)
                        control.game_controller.active.maradek_jatek -= 1

                        control.game_controller.change_active_player()
                        control.GAME_STATE = GameStates.WAITING

                        for key in scoreboard.player_calculated_scores.keys():
                            scoreboard.player_calculated_scores[key] = None

                        return
                    else:
                        logging.debug("A pontozó mező használatban van")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and control.keyboard.UP_PRESSED:
                control.keyboard.UP_PRESSED = False

            if event.key == pygame.K_DOWN and control.keyboard.DOWN_PRESSED:
                control.keyboard.DOWN_PRESSED = False

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

    scoreboard.draw_scoreboard()


def main_menu(control: GUIController) -> None:
    """
    Ez az eljárás foglalkozik a főmenüvel, a menüben megtalálható menüpontok:
        - Új játék
        - Folytatás
        - Ranklista
        - Beállítások
    """

    control.game_screen.blit(assets.main_menu_background_image, (0, 0))
    control.game_screen.blit(assets.continue_game, (550, 200))
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
                        control.STATE = State.GAME
                        control.SAVE_GAME = False

                        control.GAME_STATE = GameStates.LOADING
                        load_game(control)
                        control.GAME_STATE = GameStates.WAITING

                        # TODO: delete save
                        # have to delete save file
                        # assert "Not implemented"
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


def highscores(control: GUIController):
    """
    A ranklista menüpont, beolvassa a highscore.csv fájlból a ranklistát és kiírja
    """
    high_scores = load_high_scores()

    control.game_screen.blit(assets.high_scores_image, (0, 0))

    x1 = 140  # Játékos sora
    x2 = 620  # CPU sora
    y = 140  # A ranklista kezdősor kordinátája
    delta = 80  # A ranklista sorok közötti távolság

    control.game_screen.blit(assets.highscore_menu_font.render(f"RANKLISTA", True, assets.FontColors.cream), (480, 80))

    for i in range(5):
        rank = high_scores[i].rank
        name = high_scores[i].name
        score = high_scores[i].score
        text = f"{rank}, {name} - {score}"

        control.game_screen.blit(assets.highscore_menu_font.render(f"{text: <30}", True, assets.FontColors.cream),
                                 (x1, y + i * delta))

    for i in range(5):
        rank = high_scores[i + 5].rank
        name = high_scores[i + 5].name
        score = high_scores[i + 5].score

        text = f"{rank}, {name} - {score}"
        control.game_screen.blit(assets.highscore_menu_font.render(f"{text: <30}", True, assets.FontColors.cream),
                                 (x2, y + i * delta))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and not control.keyboard.BACKSPACE_PRESSED:
                control.keyboard.BACKSPACE_PRESSED = True
                control.STATE = State.MENU

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE and control.keyboard.BACKSPACE_PRESSED:
                control.keyboard.BACKSPACE_PRESSED = False


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
    control.game_screen.blit(assets.settings_check_box, (650, 195))

    if control.game_controller.cpu.hard_mode:
        control.game_screen.blit(assets.settings_check, (650, 195))

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


# A játék fő ciklusa
while True:

    match gui_controller.STATE:
        case State.MENU:
            main_menu(gui_controller)

        case State.GAME:
            game(gui_controller)

        case State.HIGH_SCORES:
            highscores(gui_controller)
        case State.SETTINGS:
            settings_screen(gui_controller)

    pygame.display.update()
    clock.tick(13)
