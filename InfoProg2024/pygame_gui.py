import pygame
from sys import exit

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


PLAYER_dices, CPU_dices = game_initialization.init_dices()


dices = PLAYER_dices + CPU_dices

### INIT PLAYERS ###
PLAYER_TURN = True

controller.player.dice_entities = PLAYER_dices
controller.cpu.dice_entities = CPU_dices







index = 0

def throw_state(screen, controller: Controller):

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

                print(d.is_rolling)
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
                controller.active.player_roll = False
                controller.change_active_player()

        else:
            for d in controller.active.dice_entities:
                screen.blit(d.value_image, (d.x, d.y))
                # screen.blit(dice_num_image, (250, 150))


        if not controller.active.player_roll:
            for d in controller.active.dice_entities:
                screen.blit(d.value_image, (d.x, d.y))


def game(screen, controller: Controller):

    global index

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


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and Keyboard.UP_PRESSED:
                Keyboard.UP_PRESSED = False
                print("UP UNPRESSED")

            if event.key == pygame.K_DOWN and Keyboard.DOWN_PRESSED:
                Keyboard.DOWN_PRESSED = False
                print("DOWN UNPRESSED")


    screen.blit(assets.background_image, (0, 0))
    screen.blit(assets.roll_message, (50, 300))

    screen.blit(assets.highlight_image, assets.highlight_image_rectangle)

    match GAME_STATE:
        case GameStates.DICE_THROW:
            throw_state(screen,controller)



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

