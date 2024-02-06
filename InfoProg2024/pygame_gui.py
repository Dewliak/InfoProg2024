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

STATE = State.MENU
GAME_STATE = GameStates.WAITING  # GameStates.WAITING

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

INDEX = 0
SAVE_GAME = True
MENU_POINTER = 1
MENU_SETTINGS_POINTER = 0
IS_NAME_CHANGING = False
NAME_USER_TEXT = ""


def game_keyboard_layout(screen: pygame.display):
    """
    A játék felületen az animált gombokat irányítja
    """

    # Fel
    screen.blit(assets.tooltip_font.render("Fel", True, assets.FontColors.cream), (480, 500))
    if Keyboard.UP_PRESSED:
        screen.blit(assets.keyboard_up_2, (430, 490))
    else:
        screen.blit(assets.keyboard_up_1, (430, 490))

    # Le
    screen.blit(assets.tooltip_font.render("Le", True, assets.FontColors.cream), (480, 530))
    if Keyboard.DOWN_PRESSED:
        screen.blit(assets.keyboard_down_2, (430, 520))
    else:
        screen.blit(assets.keyboard_down_1, (430, 520))

    screen.blit(assets.tooltip_font.render("Érték megadása", True, assets.FontColors.cream), (500, 555))

    # Enter
    if Keyboard.ENTER_PRESSED:
        screen.blit(assets.keyboard_enter_2, (540, 495))
    else:
        screen.blit(assets.keyboard_enter_1, (540, 495))

    screen.blit(assets.tooltip_font.render("Dobás/", True, assets.FontColors.cream), (250, 540))
    screen.blit(assets.tooltip_font.render("Következö kör", True, assets.FontColors.cream), (250, 555))

    # Space
    if Keyboard.SPACE_PRESSED:
        screen.blit(assets.keyboard_space_2, (250, 500))
    else:
        screen.blit(assets.keyboard_space_1, (250, 500))


def reset_game() -> None:
    """
    A játékot alapállapotba rakja, a játszma újraindításakor használatos
    """
    global GAME_STATE

    controller.reset()
    scoreboard.reset()

    GAME_STATE = GameStates.WAITING


def end_game(screen: pygame.display, game_controller: Controller) -> None:
    """
    A játszma befejező állapota. Ebben a részben van a pontok kiértékelése, győztes kinyilvánítása és
    a rekordok újraírása, ha szükséges. Az R betűt megnyomva újraindul a játék
    """
    global GAME_STATE
    key = pygame.key.get_pressed()

    if key[pygame.K_r]:
        reset_game()
        return

    high_scores = load_high_scores()

    screen.blit(assets.high_scores_image, (0, 0))  # háttér

    if not game_controller.high_score_save:  # Mivel ez az állapot egy loopban fut le csak első lefutáskor akarunk menteni
        if scoreboard.player_score > scoreboard.cpu_score:
            logging.info("A játékos nyert")
            high_scores = add_score_to_high_scores(high_scores, scoreboard.player_score, game_controller.player_name)
        else:
            logging.info("A CPU nyert")
            high_scores = add_score_to_high_scores(high_scores, scoreboard.cpu_score, "CPU")

        save_high_scores(high_scores)

        game_controller.high_score_save = True

    if scoreboard.player_score > scoreboard.cpu_score:
        screen.blit(assets.endgame_font.render("Nyertél", True, assets.FontColors.cream),
                    (300, 100))  # TODO: set to gold
    else:
        screen.blit(assets.endgame_font.render("Vesztettél", True, assets.FontColors.cream),
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
            assets.TextBox(screen, f"{text: ^30}", x, y + i * delta, assets.highscore_font,
                           assets.score_board_box_1).render()
        else:
            assets.TextBox(screen, f"{text: ^30}", x, y + i * delta, assets.highscore_font,
                           assets.score_board_box_2).render()

    if scoreboard.player_score > scoreboard.cpu_score:
        screen.blit(assets.font.render(f"{game_controller.player_name} - {scoreboard.player_score} pont", True,
                                       assets.FontColors.cream), (150, 250))
        screen.blit(assets.font.render(f"CPU - {scoreboard.cpu_score} pont", True, assets.FontColors.cream), (150, 320))
    else:
        screen.blit(assets.font.render(f"CPU - {scoreboard.cpu_score} pont", True, assets.FontColors.cream), (150, 250))
        screen.blit(assets.font.render(f"{game_controller.player_name} - {scoreboard.player_score} pont", True,
                                       assets.FontColors.cream), (150, 320))

    screen.blit(assets.restart_font.render("Az újra indításhoz nyomj R-t", True, assets.FontColors.cream), (180, 450))


def calculate_point(game_controller: Controller, scoreboard_object: ScoreBoard) -> None:
    """
    Két állapot van:
    Játékos van soron - ekkor dobás után kiszámolja a lehetséges mezőkre a pontszámot
                        és kiírja egy oszlopba.
    CPU van soron - ekkor a gép a saját lépést kiírja az oszlopába
    """
    global GAME_STATE

    if game_controller.active.is_cpu and GAME_STATE == GameStates.SCORING:
        chosen: Tuple[int, Callable] = game_controller.active.play_hand()

        score: int = chosen[0]
        func: Callable = chosen[1]

        scoreboard_object.create_text(score, func, ScoreType.CPU_SCORE)
        game_controller.active.player_roll = False
        game_controller.active.maradek_jatek -= 1
        GAME_STATE = GameStates.WAITING
        game_controller.change_active_player()

        return
    else:
        GAME_STATE = GameStates.PLAYER_CHOOSE

        pontok: List[Tuple[int, Callable]] = game_controller.active.ertekelesek_futtatasa()

        for p, func in pontok:
            scoreboard_object.create_text(p, func, ScoreType.CALCULATED_SCORE)


def waiting():
    """
    Dobások és értékelések közötti állapot. Vizsgálja, mikor indítjuk el a dobást
    """
    global GAME_STATE
    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        GAME_STATE = GameStates.DICE_THROW


def throw_state(screen, game_controller: Controller, scoreboard_object: ScoreBoard):
    """
    Dobás állapota, szimulálja a dobásokat és lefut a dobás animáció
    """
    global GAME_STATE

    for d in game_controller.inactive.dice_entities:
        screen.blit(d.value_image, (d.x, d.y))

    if GAME_STATE.DICE_THROW and game_controller.active.player_roll is False:
        # a player_roll az vizsgálja, hogy el vannak-e dobva a kockák

        game_controller.active.uj_dobas()

        assets.rolling_aud.play()

        game_controller.active.player_roll = True

        for i, d in enumerate(game_controller.active.dice_entities):
            game_controller.active.dice_entities[i].is_rolling = True

            game_controller.active.dice_entities[i].set_dice_value(game_controller.active.dobas.get_next())

            game_controller.active.dice_entities[i].set_image()

            # Dobás animáció
            screen.blit(game_controller.active.dice_entities[i].rolling_animation_image(), (d.x, d.y))
            game_controller.active.dice_entities[i].rolling_images_counter += 1

    else:
        if game_controller.active.player_roll:

            for i, d in enumerate(game_controller.active.dice_entities):

                if not d.is_rolling:
                    screen.blit(d.value_image, (d.x, d.y))  # rendereli a kockákat
                    continue

                screen.blit(game_controller.active.dice_entities[i].rolling_animation_image(), (d.x, d.y))

                game_controller.active.dice_entities[i].rolling_images_counter += 1

                if d.rolling_images_counter >= d.rolling_images_limit:
                    game_controller.active.dice_entities[i].is_rolling = False
                    game_controller.active.dice_entities[i].rolling_images_counter = 0

                    assets.rolling_stop_aud.play()

            if all(not x.is_rolling for x in game_controller.active.dice_entities):  # ha már az egyik kocka sem pereg
                GAME_STATE = GameStates.SCORING

                calculate_point(game_controller, scoreboard_object)

                game_controller.active.player_roll = False
        else:
            for d in game_controller.active.dice_entities:
                screen.blit(d.value_image, (d.x, d.y))

        if not game_controller.active.player_roll:  # ha nem pörögnek a kockák, akkor csak a kockákat renderelje
            for d in game_controller.active.dice_entities:
                screen.blit(d.value_image, (d.x, d.y))


def render_dices(screen: pygame.display, game_controller: Controller) -> None:
    """
    Rendereli a kockákat alap állapotukban
    """
    for d in game_controller.active.dice_entities:
        screen.blit(d.value_image, (d.x, d.y))
    for d in game_controller.inactive.dice_entities:
        screen.blit(d.value_image, (d.x, d.y))


def game(screen: pygame.display, game_controller: Controller):
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
    global INDEX, GAME_STATE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not Keyboard.UP_PRESSED:

                Keyboard.UP_PRESSED = True

                if INDEX > 0:
                    INDEX -= 1
                    assets.highlight_image_rectangle.y -= assets.HIGLIGHT_DELTA

            if event.key == pygame.K_LEFT and GAME_STATE == GAME_STATE.WAITING:
                GAME_STATE = GameStates.SAVING
                save_game(game_controller, scoreboard)
                GAME_STATE = GameStates.WAITING

                logging.info("Játék elmentve")

            if event.key == pygame.K_RIGHT and GAME_STATE == GAME_STATE.WAITING:
                GAME_STATE = GameStates.LOADING
                load_game(game_controller, scoreboard)
                GAME_STATE = GameStates.WAITING

                logging.info("Játék betöltve")

            if event.key == pygame.K_DOWN and not Keyboard.DOWN_PRESSED:
                Keyboard.DOWN_PRESSED = True

                if INDEX < settings.KOMBO_SZAM - 1:
                    INDEX += 1
                    assets.highlight_image_rectangle.y += assets.HIGLIGHT_DELTA

            if event.key == pygame.K_SPACE and not Keyboard.SPACE_PRESSED:
                Keyboard.SPACE_PRESSED = True

            if event.key == pygame.K_RETURN and not Keyboard.ENTER_PRESSED and not game_controller.active.is_cpu:
                Keyboard.ENTER_PRESSED = True

                if GAME_STATE == GameStates.PLAYER_CHOOSE:
                    # Kiválasztjuk az INDEXet, ha nincs ott még semmi beírva, akkor az adott értéket oda írjuk be

                    valasztott_kombinacio: Callable = game_controller.active.kombinaciok[INDEX]

                    if scoreboard.player_scores[valasztott_kombinacio] is None:

                        scoreboard.create_text(score=game_controller.active.kiszamolt_pontok[valasztott_kombinacio],
                                               func=valasztott_kombinacio,
                                               score_type=ScoreType.PLAYER_SCORE)
                        game_controller.active.maradek_jatek -= 1

                        game_controller.change_active_player()
                        GAME_STATE = GameStates.WAITING

                        for key in scoreboard.player_calculated_scores.keys():
                            scoreboard.player_calculated_scores[key] = None

                        return
                    else:
                        logging.debug("A pontozó mező használatban van")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and Keyboard.UP_PRESSED:
                Keyboard.UP_PRESSED = False

            if event.key == pygame.K_DOWN and Keyboard.DOWN_PRESSED:
                Keyboard.DOWN_PRESSED = False

            if event.key == pygame.K_SPACE and Keyboard.SPACE_PRESSED:
                Keyboard.SPACE_PRESSED = False

            if event.key == pygame.K_RETURN and Keyboard.ENTER_PRESSED:
                Keyboard.ENTER_PRESSED = False

    screen.blit(assets.background_image, (0, 0))  # háttér

    screen.blit(assets.highlight_image, assets.highlight_image_rectangle)  # kijelőlő téglalap

    if game_controller.active.maradek_jatek + game_controller.inactive.maradek_jatek <= 0:
        GAME_STATE = GameStates.END_GAME

    match GAME_STATE:
        case GameStates.DICE_THROW:
            throw_state(screen, game_controller, scoreboard)
        case GameStates.PLAYER_CHOOSE:
            render_dices(screen, game_controller)
        case GameStates.WAITING:
            waiting()
            render_dices(screen, game_controller)
        case GameStates.END_GAME:
            end_game(screen, game_controller)
            return

    if game_controller.player_turn:  # Rámutat arra a kocka sorra, amelyik éppen soron van
        screen.blit(assets.turn_pointer, (625, 390))
    else:
        screen.blit(assets.turn_pointer, (625, 125))

    game_keyboard_layout(screen)

    scoreboard.draw_scoreboard()


def main_menu(screen: pygame.display, game_controller: Controller) -> None:
    """
    Ez az eljárás foglalkozik a főmenüvel, a menüben megtalálható menüpontok:
        - Új játék
        - Folytatás
        - Ranklista
        - Beállítások
    """
    global SAVE_GAME, MENU_POINTER, STATE, GAME_STATE

    screen.blit(assets.main_menu_background_image, (0, 0))
    screen.blit(assets.continue_game, (550, 200))
    screen.blit(assets.new_game, (550, 280))
    screen.blit(assets.high_scores, (550, 360))
    screen.blit(assets.settings, (550, 440))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and not Keyboard.DOWN_PRESSED:
                Keyboard.DOWN_PRESSED = True
                if MENU_POINTER < 3:
                    MENU_POINTER += 1

            if event.key == pygame.K_UP and not Keyboard.UP_PRESSED:
                Keyboard.UP_PRESSED = True

                if MENU_POINTER > 0:
                    if MENU_POINTER > 1 or SAVE_GAME:
                        MENU_POINTER -= 1

            if event.key == pygame.K_RETURN and not Keyboard.ENTER_PRESSED:
                match MENU_POINTER:
                    case 0:  # Folytatás
                        STATE = State.GAME
                        SAVE_GAME = False

                        GAME_STATE = GameStates.LOADING
                        load_game(game_controller, scoreboard)
                        GAME_STATE = GameStates.WAITING

                        # TODO: delete save
                        # have to delete save file
                        # assert "Not implemented"
                    case 1:  # Új játék
                        reset_game()
                        STATE = State.GAME
                        GAME_STATE = GameStates.WAITING
                    case 2:  # Ranklista
                        STATE = State.HIGH_SCORES
                    case 3:  # Beállítások
                        STATE = State.SETTINGS

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and Keyboard.DOWN_PRESSED:
                Keyboard.DOWN_PRESSED = False

            if event.key == pygame.K_UP and Keyboard.UP_PRESSED:
                Keyboard.UP_PRESSED = False

            if event.key == pygame.K_RETURN and Keyboard.ENTER_PRESSED:
                Keyboard.ENTER_PRESSED = False

    screen.blit(assets.menu_pointer_image, (480, 200 + 80 * MENU_POINTER))  # Menü mutató


def highscores(screen: pygame.display):
    """
    A ranklista menüpont, beolvassa a highscore.csv fájlból a ranklistát és kiírja
    """
    global STATE
    high_scores = load_high_scores()

    screen.blit(assets.high_scores_image, (0, 0))

    x1 = 140  # Játékos sora
    x2 = 620  # CPU sora
    y = 140  # A ranklista kezdősor kordinátája
    delta = 80  # A ranklista sorok közötti távolság
    
    screen.blit(assets.highscore_menu_font.render(f"RANKLISTA", True, assets.FontColors.cream), (480, 80))
    
    for i in range(5):
        rank = high_scores[i].rank
        name = high_scores[i].name
        score = high_scores[i].score
        text = f"{rank}, {name} - {score}"

        screen.blit(assets.highscore_menu_font.render(f"{text: <30}", True, assets.FontColors.cream),
                    (x1, y + i * delta))

    for i in range(5):
        rank = high_scores[i + 5].rank
        name = high_scores[i + 5].name
        score = high_scores[i + 5].score

        text = f"{rank}, {name} - {score}"
        screen.blit(assets.highscore_menu_font.render(f"{text: <30}", True, assets.FontColors.cream),
                    (x2, y + i * delta))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and not Keyboard.BACKSPACE_PRESSED:
                Keyboard.BACKSPACE_PRESSED = True
                STATE = State.MENU

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE and Keyboard.BACKSPACE_PRESSED:
                Keyboard.BACKSPACE_PRESSED = False


def settings_screen(screen: pygame.display, game_controller: Controller) -> None:
    """
    Beállításuk menüpont, itt található beállítások:
        - Nehézség - HARDMODE, vagy EASYMODE
        - Név - Enter lenyomásával átírható 
    """
    global IS_NAME_CHANGING, MENU_SETTINGS_POINTER, NAME_USER_TEXT, STATE

    screen.blit(assets.settings_image, (0, 0))

    if IS_NAME_CHANGING:  # Név váltás

        screen.blit(assets.highlight_image, (430, 295))
        screen.blit(assets.highscore_menu_font.render(str(NAME_USER_TEXT), True, assets.FontColors.cream),
                    (545, 300))
    else:
        screen.blit(assets.highscore_menu_font.render(str(game_controller.player_name), True, assets.FontColors.cream),
                    (545, 300))

    # Beállítások kiírása

    screen.blit(assets.menu_pointer_image, (400, 200 + 100 * MENU_SETTINGS_POINTER))
    
    screen.blit(assets.highscore_menu_font.render(f"Name:", True, assets.FontColors.cream), (440, 300))

    screen.blit(assets.highscore_menu_font.render("Hardmode", True, assets.FontColors.cream), (440, 200))
    screen.blit(assets.settings_check_box, (650, 195))
    
    if game_controller.cpu.hard_mode:
        screen.blit(assets.settings_check, (650, 195))

    for event in pygame.event.get():
        
        if IS_NAME_CHANGING:
            """
            Név változás folyamat, figyeli mely betűket nyomunk le, lehetséges a törlés is
            """
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    NAME_USER_TEXT = NAME_USER_TEXT[:-1]

                elif event.key == pygame.K_RETURN and NAME_USER_TEXT.strip() != "":
                    IS_NAME_CHANGING = False
                    game_controller.player_name = NAME_USER_TEXT

                else:
                    if not (NAME_USER_TEXT.strip() == "" and event.unicode == " "):
                        NAME_USER_TEXT += event.unicode
        else:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and not Keyboard.DOWN_PRESSED:
                    Keyboard.DOWN_PRESSED = True
                    if MENU_SETTINGS_POINTER < 1:
                        MENU_SETTINGS_POINTER += 1

                if event.key == pygame.K_UP and not Keyboard.UP_PRESSED:
                    Keyboard.UP_PRESSED = True

                    if MENU_SETTINGS_POINTER > 0:
                        MENU_SETTINGS_POINTER -= 1

                if event.key == pygame.K_RETURN and not Keyboard.ENTER_PRESSED:

                    match MENU_SETTINGS_POINTER:
                        case 0:  # HARDMODE

                            if game_controller.cpu.hard_mode:
                                game_controller.cpu.set_easy_mode()
                            else:
                                game_controller.cpu.set_hard_mode()

                        case 1:  # Név változtatás
                            if not IS_NAME_CHANGING:
                                IS_NAME_CHANGING = True
                            NAME_USER_TEXT = ""
                            game_controller.player_name = NAME_USER_TEXT

                if event.key == pygame.K_BACKSPACE and not Keyboard.BACKSPACE_PRESSED:
                    Keyboard.BACKSPACE_PRESSED = True
                    STATE = State.MENU

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN and Keyboard.DOWN_PRESSED:
                    Keyboard.DOWN_PRESSED = False

                if event.key == pygame.K_UP and Keyboard.UP_PRESSED:
                    Keyboard.UP_PRESSED = False

                if event.key == pygame.K_RETURN and Keyboard.ENTER_PRESSED:
                    Keyboard.ENTER_PRESSED = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE and Keyboard.BACKSPACE_PRESSED:
                        Keyboard.BACKSPACE_PRESSED = False


# A játék fő ciklusa
while True:

    match STATE:
        case State.MENU:
            main_menu(game_screen, controller)

        case State.GAME:
            game(game_screen, controller)

        case State.HIGH_SCORES:
            highscores(game_screen)
        case State.SETTINGS:
            settings_screen(game_screen, controller)

    pygame.display.update()
    clock.tick(13)
