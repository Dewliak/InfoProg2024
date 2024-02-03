import pprint

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

STATE = State.MENU
GAME_STATE = GameStates.WAITING #GameStates.WAITING

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Kockapóker")

from utilities import assets
from utilities.scoreboard import ScoreBoard, ScoreType
#from utilities import keyboard_layout
PLAYER_dices, CPU_dices = game_initialization.init_dices()


dices = PLAYER_dices + CPU_dices

### INIT PLAYERS ###
scoreboard = ScoreBoard(screen)
controller.player.dice_entities = PLAYER_dices
controller.cpu.dice_entities = CPU_dices
controller.cpu.set_hard_mode()
index = 0

def game_keyboard_layout(screen):

    # up pressed
    screen.blit(assets.tooltip_font.render("Fel", True, assets.FontColors.cream), (480,500))
    if Keyboard.UP_PRESSED:
        screen.blit(assets.keyboard_up_2, (430,490))
    else:
        screen.blit(assets.keyboard_up_1, (430, 490))

    screen.blit(assets.tooltip_font.render("Le", True, assets.FontColors.cream), (480, 530))
    if Keyboard.DOWN_PRESSED:
        screen.blit(assets.keyboard_down_2, (430,520))
    else:
        screen.blit(assets.keyboard_down_1, (430, 520))

    screen.blit(assets.tooltip_font.render("Érték megadása", True, assets.FontColors.cream), (500, 555))
    if Keyboard.ENTER_PRESSED:
        screen.blit(assets.keyboard_enter_2, (540,495))
    else:
        screen.blit(assets.keyboard_enter_1, (540, 495))

    screen.blit(assets.tooltip_font.render("Dobás/", True, assets.FontColors.cream), (250, 540))
    screen.blit(assets.tooltip_font.render("Következö kör", True, assets.FontColors.cream), (250, 555))
    if Keyboard.SPACE_PRESSED:
        screen.blit(assets.keyboard_space_2, (250, 500))
    else:
        screen.blit(assets.keyboard_space_1, (250, 500))




def reset_game():
    global GAME_STATE

    controller.reset()
    scoreboard.reset()


    GAME_STATE = GameStates.WAITING

def end_game(screen, controller):
    global GAME_STATE
    key = pygame.key.get_pressed()

    if key[pygame.K_r]:
        reset_game()
        print("r")
        return


    high_scores = load_high_scores()

    screen.blit(assets.high_scores_image, (0, 0))
    if not controller.high_score_save:
        if scoreboard.player_score > scoreboard.cpu_score:
            print("Player wins")
            high_scores = add_score_to_high_scores(high_scores, scoreboard.player_score, controller.player_name)
        else:
            print("CPU wins")
            high_scores = add_score_to_high_scores(high_scores, scoreboard.cpu_score, "CPU")

        save_high_scores(high_scores)

        controller.high_score_save = True

    win_lost_x = 150
    win_lost_y = 40



    if scoreboard.player_score > scoreboard.cpu_score:
        screen.blit(assets.endgame_font.render("Nyertél", True, assets.FontColors.cream),(300,100))  # TODO: set to gold
    else:
        screen.blit(assets.endgame_font.render("Vesztettél", True, assets.FontColors.cream),(300,100))  # TODO: set to gold
    x1 = 660 # player score x coord
    x2 = 910#1000 # cpu score x coord
    y = 80#50
    delta = 50#70

    for i in range(10):
        rank = high_scores[i].rank
        name = high_scores[i].name
        score = high_scores[i].score
        text = f"{rank}, {name} - {score}"
        if i % 2 == 0:
            # screen.blit(assets.score_board_box_1, (460,20+i*75))
            assets.TextBox(screen, f"{text : ^30}", x2, y + i * delta, assets.highscore_font,
                           assets.score_board_box_1).render()
        else:
            assets.TextBox(screen, f"{text: ^30}", x2, y + i * delta, assets.highscore_font,
                           assets.score_board_box_2).render()

    if scoreboard.player_score > scoreboard.cpu_score:
        screen.blit(assets.font.render(f"{controller.player_name} - {scoreboard.player_score} pont", True,
                                       assets.FontColors.cream), (150, 250))
        screen.blit(assets.font.render(f"CPU - {scoreboard.cpu_score} pont", True, assets.FontColors.cream), (150, 320))
    else:
        screen.blit(assets.font.render(f"CPU - {scoreboard.cpu_score} pont", True, assets.FontColors.cream), (150, 250))
        screen.blit(assets.font.render(f"{controller.player_name} - {scoreboard.player_score} pont", True,
                                       assets.FontColors.cream), (150, 320))

    #assets.TextBox(screen, f"{controller.player_name} - {scoreboard.player_score} pont", 300, 250, assets.highscore_font,
    #                   assets.score_board_box_1).render()
    #assets.TextBox(screen, f"CPU - {scoreboard.cpu_score} pont", 300, 320, assets.highscore_font,
    #               assets.score_board_box_1).render()

    screen.blit(assets.restart_font.render("Az újra indításhoz nyomj R-t", True, assets.FontColors.cream), (180, 450))


def calculate_point(screen, controller: Controller, scoreboard: ScoreBoard) -> None:
    global GAME_STATE
    if controller.active.is_cpu and GAME_STATE == GameStates.SCORING  :
        chosen: Tuple[int, Callable] = controller.active.play_hand()

        score: int = chosen[0]
        func: Callable = chosen[1]

        scoreboard.create_text(score, func, ScoreType.CPU_SCORE)
        controller.active.player_roll = False
        controller.active.maradek_jatek -= 1
        GAME_STATE = GameStates.WAITING
        controller.change_active_player()



        return
    else:
        GAME_STATE = GameStates.PLAYER_CHOOSE

        pontok: List[Tuple[int, Callable]] = controller.active.ertekelesek_futtatasa()

        for p,func in pontok:
            scoreboard.create_text(p, func, ScoreType.CALCULATED_SCORE)






def waiting(screen, controller):
    global GAME_STATE
    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        GAME_STATE = GameStates.DICE_THROW




    if key[pygame.K_F1]:
        reset_game()
        print("F1")

def throw_state(screen, controller: Controller, scoreboard: ScoreBoard):
    global GAME_STATE
    key = pygame.key.get_pressed()

    for d in controller.inactive.dice_entities:
        screen.blit(d.value_image, (d.x, d.y))

    if GAME_STATE.DICE_THROW and controller.active.player_roll is False:

        controller.active.uj_dobas()

        assets.rolling_aud.play()

        controller.active.player_roll = True

        for i, d in enumerate(controller.active.dice_entities):
            controller.active.dice_entities[i].is_rolling = True

            controller.active.dice_entities[i].set_dice_value(controller.active.dobas.get_next())

            controller.active.dice_entities[i].set_image()

            screen.blit(controller.active.dice_entities[i].rolling_animation_image(), (d.x, d.y))
            # screen.blit(dice_rolling_images[rolling_images_counter], (250, 150))
            controller.active.dice_entities[i].rolling_images_counter += 1
            # rolling_images_counter += 1
    else:
        if controller.active.player_roll:

            for i, d in enumerate(controller.active.dice_entities):


                if not d.is_rolling:
                    screen.blit(d.value_image, (d.x, d.y))
                    continue

                screen.blit(controller.active.dice_entities[i].rolling_animation_image(), (d.x, d.y))

                controller.active.dice_entities[i].rolling_images_counter += 1

                if d.rolling_images_counter >= d.rolling_images_limit:
                    controller.active.dice_entities[i].is_rolling = False
                    controller.active.dice_entities[i].rolling_images_counter = 0

                    assets.rolling_stop_aud.play()

            if all(not x.is_rolling for x in controller.active.dice_entities):

                GAME_STATE = GameStates.SCORING

                calculate_point(screen, controller, scoreboard)

                controller.active.player_roll = False

                #SCORE?!





        else:
            for d in controller.active.dice_entities:
                screen.blit(d.value_image, (d.x, d.y))
                # screen.blit(dice_num_image, (250, 150))


        if not controller.active.player_roll:
            for d in controller.active.dice_entities:
                screen.blit(d.value_image, (d.x, d.y))


def render_dices(screen, controller):



    for d in controller.active.dice_entities:
        screen.blit(d.value_image, (d.x, d.y))
        # screen.blit(dice_num_image, (250, 150))
    for d in controller.inactive.dice_entities:
        screen.blit(d.value_image, (d.x, d.y))


def game(screen, controller: Controller):

    global index,GAME_STATE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not Keyboard.UP_PRESSED:

                Keyboard.UP_PRESSED = True
                print("UP PRESSED")

                if index > 0:
                    index -= 1
                    assets.highlight_image_rectangle.y -= assets.HIGLIGHT_DELTA

            if event.key == pygame.K_LEFT and GAME_STATE == GAME_STATE.WAITING:
                GAME_STATE = GameStates.SAVING
                save_game(controller, scoreboard)
                GAME_STATE = GameStates.WAITING
                print("DATA SAVED")

            if event.key == pygame.K_RIGHT and GAME_STATE == GAME_STATE.WAITING:
                GAME_STATE = GameStates.LOADING
                load_game(controller, scoreboard)
                GAME_STATE = GameStates.WAITING
                print("DATA LOADED")

            if event.key == pygame.K_DOWN and not Keyboard.DOWN_PRESSED:
                Keyboard.DOWN_PRESSED = True
                print("DOWN PRESSED")

                if index < settings.KOMBO_SZAM - 1:
                    index += 1
                    assets.highlight_image_rectangle.y += assets.HIGLIGHT_DELTA
                print(index)

            if event.key == pygame.K_SPACE and not Keyboard.SPACE_PRESSED:
                print("SPACE PRESSED")
                Keyboard.SPACE_PRESSED = True

            if event.key == pygame.K_RETURN and not Keyboard.ENTER_PRESSED and not controller.active.is_cpu:
                Keyboard.ENTER_PRESSED = True

                if GAME_STATE == GameStates.PLAYER_CHOOSE:
                    #kivalasztjuk az indexet, ha nincs ott mar beirva valami ,akkor az adott erteket irjuk be

                    choosen_index: int = index

                    valasztott_kombinacio: Callable = controller.active.kombinaciok[index]

                    if scoreboard.player_scores[valasztott_kombinacio] is None:
                        pont: int = scoreboard.player_calculated_scores[valasztott_kombinacio]
                        scoreboard.create_text(score = controller.active.kiszamolt_pontok[valasztott_kombinacio],
                                               func = valasztott_kombinacio,
                                               score_type= ScoreType.PLAYER_SCORE)
                        controller.active.maradek_jatek -= 1

                        controller.change_active_player()
                        GAME_STATE = GameStates.WAITING

                        for key in scoreboard.player_calculated_scores.keys():
                            scoreboard.player_calculated_scores[key] = None

                        return
                    else:
                        print("Hasznalatban van")




        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and Keyboard.UP_PRESSED:
                Keyboard.UP_PRESSED = False
                print("UP UNPRESSED")

            if event.key == pygame.K_DOWN and Keyboard.DOWN_PRESSED:
                Keyboard.DOWN_PRESSED = False
                print("DOWN UNPRESSED")

            if event.key == pygame.K_SPACE and Keyboard.SPACE_PRESSED:
                Keyboard.SPACE_PRESSED = False

            if event.key == pygame.K_RETURN and Keyboard.ENTER_PRESSED:
                Keyboard.ENTER_PRESSED = False



    screen.blit(assets.background_image, (0, 0))


    screen.blit(assets.highlight_image, assets.highlight_image_rectangle)

    if controller.active.maradek_jatek + controller.inactive.maradek_jatek <= 0:
        GAME_STATE = GameStates.END_GAME

    match GAME_STATE:
        case GameStates.DICE_THROW:
            throw_state(screen,controller, scoreboard)
        case GameStates.PLAYER_CHOOSE:
            render_dices(screen, controller)
        case GameStates.WAITING:
            waiting(screen, controller)
            render_dices(screen, controller)
        case GameStates.END_GAME:
            end_game(screen, controller)
            print("END GAME")
            return

    if controller.player_turn:
        screen.blit(assets.turn_pointer, (625,390))
    else:
        screen.blit(assets.turn_pointer, (625, 125))

    game_keyboard_layout(screen)

    scoreboard.draw_scoreboard()

def player_choose(screen, controller, scoreboard) -> None:
    pass

def main_menu(screen, controller):

    global SAVE_GAME, MENU_POINTER, STATE, GAME_STATE



    screen.blit(assets.main_menu_background_image, (0, 0))
    screen.blit(assets.continue_game, (550, 200))
    screen.blit(assets.new_game,(550,280))
    screen.blit(assets.high_scores, (550, 360))
    screen.blit(assets.settings, (550, 440))

    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and not Keyboard.DOWN_PRESSED:
                Keyboard.DOWN_PRESSED = True
                if MENU_POINTER < 3:
                    MENU_POINTER += 1
                print("DOWN HERE")

            if event.key == pygame.K_UP and not Keyboard.UP_PRESSED:
                Keyboard.UP_PRESSED = True

                if MENU_POINTER > 0:
                    if MENU_POINTER > 1 or SAVE_GAME:
                        MENU_POINTER -= 1


                print("HUP ERE")

            if event.key == pygame.K_RETURN and not Keyboard.ENTER_PRESSED:
                match MENU_POINTER:
                    case 0:
                        # load game and st# art
                        STATE = State.GAME
                        SAVE_GAME = False

                        GAME_STATE = GameStates.LOADING
                        load_game(controller, scoreboard)
                        GAME_STATE = GameStates.WAITING

                        # TODO: delete save
                        # have to delete save file
                        #assert "Not implemented"
                    case 1:
                        reset_game()
                        STATE = State.GAME
                        GAME_STATE = GameStates.WAITING
                    case 2: #high score
                        STATE = State.HIGH_SCORES
                    case 3: # settings
                        STATE = State.SETTINGS



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and Keyboard.DOWN_PRESSED:
                Keyboard.DOWN_PRESSED = False
                print("UNpresed")

            if event.key == pygame.K_UP and Keyboard.UP_PRESSED:
                Keyboard.UP_PRESSED = False
                print("UNpresed")

            if event.key == pygame.K_RETURN and Keyboard.ENTER_PRESSED:
                Keyboard.ENTER_PRESSED = False

    screen.blit(assets.menu_pointer_image, (480, 200 + 80 * MENU_POINTER))

def highscores(screen, controller):
    global STATE
    high_scores = load_high_scores()

    screen.blit(assets.high_scores_image, (0,0))

    x1 = 140  # player score x coord
    x2 = 620  # cpu score x coord
    y = 140
    delta = 80
    screen.blit(assets.highscore_menu_font.render(f"RANGLISTA", True, assets.FontColors.cream), (480,80))
    for i in range(5):
        rank = high_scores[i].rank
        name = high_scores[i].name
        score = high_scores[i].score
        text = f"{rank}, {name} - {score}"

        screen.blit(assets.highscore_menu_font.render(f"{text : <30}", True, assets.FontColors.cream),(x1, y + i * delta))


    for i in range(5):
        rank = high_scores[i + 5].rank
        name = high_scores[i + 5].name
        score = high_scores[i + 5].score

        text = f"{rank}, {name} - {score}"
        screen.blit(assets.highscore_menu_font.render(f"{text : <30}", True, assets.FontColors.cream),(x2, y + i * delta))

    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and not Keyboard.BACKSPACE_PRESSED:
                Keyboard.BACKSPACE_PRESSED = True
                STATE = State.MENU

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE and  Keyboard.BACKSPACE_PRESSED:
                Keyboard.BACKSPACE_PRESSED = False


def settings_screen(screen, controller):
    global IS_NAME_CHANGING, MENU_SETTINGS_POINTER, NAME_USER_TEXT, STATE

    screen.blit(assets.settings_image, (0,0))

    if IS_NAME_CHANGING:

        screen.blit(assets.highlight_image, (430,295))
        screen.blit(assets.highscore_menu_font.render(str(NAME_USER_TEXT), True, assets.FontColors.cream),
                    (545, 300))
    else:
        screen.blit(assets.highscore_menu_font.render(str(controller.player_name), True, assets.FontColors.cream),
                    (545, 300))

    # RENDER TEXT
    screen.blit(assets.highscore_menu_font.render("Hardmode", True, assets.FontColors.cream),(440,200))
    screen.blit(assets.highscore_menu_font.render(f"Name:", True, assets.FontColors.cream),(440, 300))

    screen.blit(assets.menu_pointer_image, (400, 200 + 100 * MENU_SETTINGS_POINTER))

    screen.blit(assets.settings_check_box, (650, 195))

    if controller.cpu.hard_mode:
        screen.blit(assets.settings_check, (650, 195))

    for event in pygame.event.get():

        if IS_NAME_CHANGING:
            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    NAME_USER_TEXT = NAME_USER_TEXT[:-1]

                    # Unicode standard is used for string
                # formation
                elif event.key == pygame.K_RETURN and NAME_USER_TEXT.strip() != "":
                    IS_NAME_CHANGING = False
                    controller.player_name = NAME_USER_TEXT

                else:
                    # space, ures
                    # ures es space
                    # ures es nem space jo
                    # nem ures es space jo
                    # nem ures es nem space jo

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
                    print("DOWN HERE")

                if event.key == pygame.K_UP and not Keyboard.UP_PRESSED:
                    Keyboard.UP_PRESSED = True

                    if MENU_SETTINGS_POINTER > 0:
                        MENU_SETTINGS_POINTER -= 1

                    print("HUP ERE")

                if event.key == pygame.K_RETURN and not Keyboard.ENTER_PRESSED:

                    match MENU_SETTINGS_POINTER:
                        case 0: # HARDMODE

                            if controller.cpu.hard_mode:
                                controller.cpu.set_easy_mode()
                            else:
                                controller.cpu.set_hard_mode()

                        case 1: # CHANGE NAME
                            if not IS_NAME_CHANGING:
                                IS_NAME_CHANGING = True
                            NAME_USER_TEXT = ""
                            controller.player_name = NAME_USER_TEXT

                if event.key == pygame.K_BACKSPACE and not Keyboard.BACKSPACE_PRESSED:
                        Keyboard.BACKSPACE_PRESSED = True
                        STATE = State.MENU

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN and Keyboard.DOWN_PRESSED:
                    Keyboard.DOWN_PRESSED = False
                    print("UNpresed")

                if event.key == pygame.K_UP and Keyboard.UP_PRESSED:
                    Keyboard.UP_PRESSED = False
                    print("UNpresed")

                if event.key == pygame.K_RETURN and Keyboard.ENTER_PRESSED:
                    Keyboard.ENTER_PRESSED = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE and Keyboard.BACKSPACE_PRESSED:
                        Keyboard.BACKSPACE_PRESSED = False

SAVE_GAME = True
MENU_POINTER = 1
MENU_SETTINGS_POINTER = 0
IS_NAME_CHANGING = False
NAME_USER_TEXT = ""
#t = assets.TextBox(screen, assets.GameText.end_game_text_player_win.format(name=controller.player_name),300, 400, assets.font, assets.text_box)
while True:

    match STATE:
        case State.MENU:
            main_menu(screen, controller)

        case State.GAME:
            game(screen, controller)

        case State.HIGH_SCORES:
            highscores(screen, controller)
        case State.SETTINGS:
            settings_screen(screen, controller)

    #t.render()

    pygame.display.update()
    clock.tick(13)

