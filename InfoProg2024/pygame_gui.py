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

from utilities.gui_controller import GUIController
from InfoProg2024.utilities.game_state_modules.game import game
from InfoProg2024.utilities.menu_state_modules.highscores import highscores
from InfoProg2024.utilities.menu_state_modules.main_menu import main_menu
from InfoProg2024.utilities.menu_state_modules.settings_screen import settings_screen
from InfoProg2024.utilities.menu_state_modules.hello_screen import hello_screen
PLAYER_dices, CPU_dices = game_initialization.init_dices()

dices = PLAYER_dices + CPU_dices

# Fő változók inicializálása
pygame.display.set_icon(assets.icon)
scoreboard = ScoreBoard(game_screen)

controller.player.dice_entities = PLAYER_dices
controller.cpu.dice_entities = CPU_dices
controller.cpu.set_hard_mode()

gui_controller = GUIController(game_screen, controller, scoreboard)



# A játék fő ciklusa
while True:
    #print(gui_controller.STATE.value is State.MENU.value)
    match gui_controller.STATE.value:
        case State.HELLO_SCREEN.value:
            hello_screen(gui_controller)

        case State.MENU.value:
            main_menu(gui_controller)

            #print("this")

        case State.GAME.value:
            #print("here2")
            game(gui_controller)


        case State.HIGH_SCORES.value:
            highscores(gui_controller)
        case State.SETTINGS.value:
            settings_screen(gui_controller)



    #gui_controller.game_screen.display.update()
    pygame.display.update()
    clock.tick(13)
