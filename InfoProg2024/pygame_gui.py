import pygame
from sys import exit
from typing import Tuple, Callable, List
from InfoProg2024.modulok.player import controller, Controller


from utilities.keyboard_press import Keyboard
from utilities.states import State, GameStates
from utilities import game_initialization


from utilities.settings import settings

STATE = State.GAME
GAME_STATE = GameStates.DICE_THROW

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Kockapóker")

from utilities import assets
from utilities.scoreboard import ScoreBoard, ScoreType

PLAYER_dices, CPU_dices = game_initialization.init_dices()


dices = PLAYER_dices + CPU_dices

### INIT PLAYERS ###
scoreboard = ScoreBoard(screen)
controller.player.dice_entities = PLAYER_dices
controller.cpu.dice_entities = CPU_dices
controller.cpu.set_hard_mode()
index = 0

def calculate_point(screen, controller: Controller, scoreboard: ScoreBoard) -> None:
    global GAME_STATE
    if controller.active.is_cpu and GAME_STATE == GameStates.SCORING  :
        chosen: Tuple[int, Callable] = controller.active.play_hand()

        score: int = chosen[0]
        func: Callable = chosen[1]

        scoreboard.create_text(score, func, ScoreType.CPU_SCORE)
        controller.active.player_roll = False
        controller.active.maradek_jatek -= 1
        GAME_STATE = GameStates.DICE_THROW
        controller.change_active_player()



        return
    else:
        GAME_STATE = GameStates.PLAYER_CHOOSE

        pontok: List[Tuple[int, Callable]] = controller.active.ertekelesek_futtatasa()

        for p,func in pontok:
            scoreboard.create_text(p, func, ScoreType.CALCULATED_SCORE)









def throw_state(screen, controller: Controller, scoreboard: ScoreBoard):
    global GAME_STATE
    key = pygame.key.get_pressed()

    for d in controller.inactive.dice_entities:
        screen.blit(d.value_image, (d.x, d.y))

    if key[pygame.K_SPACE] and controller.active.player_roll is False:

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

    if controller.active.maradek_jatek + controller.inactive.maradek_jatek <= 0:
        GAME_STATE = GameStates.END_GAME

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

            if event.key == pygame.K_DOWN and not Keyboard.DOWN_PRESSED:
                Keyboard.DOWN_PRESSED = True
                print("DOWN PRESSED")

                if index < settings.KOMBO_SZAM - 1:
                    index += 1
                    assets.highlight_image_rectangle.y += assets.HIGLIGHT_DELTA
                print(index)

            if event.key == pygame.K_RETURN and not Keyboard.SPACE_PRESSED and not controller.active.is_cpu:
                Keyboard.SPACE_PRESSED = True

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
                        GAME_STATE = GameStates.DICE_THROW

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

            if event.key == pygame.K_RETURN and Keyboard.SPACE_PRESSED:
                Keyboard.SPACE_PRESSED = False

    screen.blit(assets.background_image, (0, 0))
    screen.blit(assets.roll_message, (50, 300))

    screen.blit(assets.highlight_image, assets.highlight_image_rectangle)

    match GAME_STATE:
        case GameStates.DICE_THROW:
            throw_state(screen,controller, scoreboard)
        case GameStates.PLAYER_CHOOSE:
            render_dices(screen, controller)
        case GameStates.END_GAME:
            print("END GAME")

    scoreboard.draw_scoreboard()

def player_choose(screen, controller, scoreboard) -> None:
    pass

while True:

    match STATE:
        case State.MENU:
            pass

        case State.GAME:
            game(screen, controller)

        case State.HIGH_SCORES:
            pass






    pygame.display.update()
    clock.tick(13)

