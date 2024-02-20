import pygame
import logging

from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities import assets

from InfoProg2024.utilities.game_state_modules.reset_game import reset_game

from InfoProg2024.utilities.high_score import save_high_scores, load_high_scores, add_score_to_high_scores



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



        if control.game_scoreboard.player_score > control.game_scoreboard.cpu_score:

            if high_scores[-1].score < control.game_scoreboard.player_score:
                control.game_scoreboard.IS_SAVING_TO_HIHSCORES = True
            else:
                control.game_scoreboard.IS_SAVING_TO_HIHSCORES = False

            logging.info("A játékos nyert")
            high_scores = add_score_to_high_scores(high_scores, control.game_scoreboard.player_score,
                                                   control.game_controller.player_name)
        else:
            logging.info("A CPU nyert")

            if high_scores[-1].score < control.game_scoreboard.player_score:
                control.game_scoreboard.IS_SAVING_TO_HIHSCORES = True
            else:
                control.game_scoreboard.IS_SAVING_TO_HIHSCORES = False

            high_scores = add_score_to_high_scores(high_scores, control.game_scoreboard.cpu_score, "CPU")

        save_high_scores(high_scores)

        control.game_controller.high_score_save = True

    if control.game_scoreboard.player_score > control.game_scoreboard.cpu_score:
        control.game_screen.blit(assets.endgame_font.render("Nyertél", True, assets.FontColors.cream),
                                 (300, 100))  # TODO: set to gold
    else:
        control.game_screen.blit(assets.endgame_font.render("Vesztettél", True, assets.FontColors.cream),
                                 (300, 100))  # TODO: set to gold

    x = 910  # Ranksor koordináták
    y = 80
    delta = 50

    if control.game_scoreboard.IS_SAVING_TO_HIHSCORES:
        control.game_screen.blit(assets.tooltip_font.render("A gyoztes pontszám felkerult a ranglistára", True,
                                assets.FontColors.cream),(150,400))
    else:
        control.game_screen.blit(assets.tooltip_font.render("Nem lett eleg pont a ranglistához", True,
                                assets.FontColors.cream), (150,400))


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

    if control.game_scoreboard.player_score > control.game_scoreboard.cpu_score:
        control.game_screen.blit(
            assets.font.render(f"{control.game_controller.player_name} - {control.game_scoreboard.player_score} pont", True,
                               assets.FontColors.cream), (150, 250))
        control.game_screen.blit(
            assets.font.render(f"CPU - {control.game_scoreboard.cpu_score} pont", True, assets.FontColors.cream),
            (150, 320))
    else:
        control.game_screen.blit(
            assets.font.render(f"CPU - {control.game_scoreboard.cpu_score} pont", True, assets.FontColors.cream),
            (150, 250))
        control.game_screen.blit(
            assets.font.render(f"{control.game_controller.player_name} - {control.game_scoreboard.player_score} pont", True,
                               assets.FontColors.cream), (150, 320))

    control.game_screen.blit(assets.restart_font.render("Az újra indításhoz nyomj R-t", True, assets.FontColors.cream),
                             (180, 450))
