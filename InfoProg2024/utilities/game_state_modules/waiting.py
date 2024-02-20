import pygame

from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities.states import GameStates


def waiting(control: GUIController):
    """
    Dobások és értékelések közötti állapot. Vizsgálja, mikor indítjuk el a dobást
    """

    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        control.GAME_STATE = GameStates.DICE_THROW
