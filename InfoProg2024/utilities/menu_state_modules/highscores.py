import pygame

from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities import assets
from InfoProg2024.utilities.high_score import load_high_scores
from InfoProg2024.utilities.states import State


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
