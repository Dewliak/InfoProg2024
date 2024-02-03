import pygame
from sys import exit

from InfoProg2024.modulok.dobas_modul import DobasData
from InfoProg2024.modulok.kocka import Dice, DiceImages, DEFAULT_ROLLING_LENGTH, DEFUALT_ROLLING_INTERVAL

from enum import Enum

class GameStates(Enum):
    DICE_THROW = 1
    SCORING = 2
    END_GAME = 3
