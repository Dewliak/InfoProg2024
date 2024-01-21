from InfoProg2024.modulok.dobas_modul.dobas_ertekelo import DobasErtekelo
from .assets import font, FontColors

from typing import Callable
from enum import Enum


class ScoreType(Enum):
    PLAYER_SCORE = 1
    CALCULATED_SCORE = 2
    CPU_SCORE = 3


class ScoreBoard:
    start_y_coordinate = 96
    y_interval = 47

    def   __init__(self, screen):

        self.screen = screen

        self.player_score = 0
        self.cpu_score = 0

        # TODO: test
        self.player_column = 900
        self.calculation_column = 1000
        self.cpu_column = 1110

        self.player_score_pos_y = 515
        self.cpu_score_pos_y = 515

        self.player_scores = {DobasErtekelo.tetszoleges_kombinacio: None,
                              DobasErtekelo.par: None,
                              DobasErtekelo.drill: None,
                              DobasErtekelo.ket_par: None,
                              DobasErtekelo.full: None,
                              DobasErtekelo.kis_sor: None,
                              DobasErtekelo.nagy_sor: None,
                              DobasErtekelo.kis_poker: None,
                              DobasErtekelo.nagy_poker: None
                              }

        self.player_calculated_scores = {DobasErtekelo.tetszoleges_kombinacio: None,
                                         DobasErtekelo.par: None,
                                         DobasErtekelo.drill: None,
                                         DobasErtekelo.ket_par: None,
                                         DobasErtekelo.full: None,
                                         DobasErtekelo.kis_sor: None,
                                         DobasErtekelo.nagy_sor: None,
                                         DobasErtekelo.kis_poker: None,
                                         DobasErtekelo.nagy_poker: None,
                                         }

        self.cpu_scores = {DobasErtekelo.tetszoleges_kombinacio: None,
                           DobasErtekelo.par: None,
                           DobasErtekelo.drill: None,
                           DobasErtekelo.ket_par: None,
                           DobasErtekelo.full: None,
                           DobasErtekelo.kis_sor: None,
                           DobasErtekelo.nagy_sor: None,
                           DobasErtekelo.kis_poker: None,
                           DobasErtekelo.nagy_poker: None
                           }

        self.y_coordinate = {DobasErtekelo.tetszoleges_kombinacio: ScoreBoard.start_y_coordinate,
                             DobasErtekelo.par: ScoreBoard.start_y_coordinate + ScoreBoard.y_interval,
                             DobasErtekelo.drill: ScoreBoard.start_y_coordinate + 2 * ScoreBoard.y_interval,
                             DobasErtekelo.ket_par: ScoreBoard.start_y_coordinate + 3 * ScoreBoard.y_interval,
                             DobasErtekelo.full: ScoreBoard.start_y_coordinate + 4 * ScoreBoard.y_interval,
                             DobasErtekelo.kis_sor: ScoreBoard.start_y_coordinate + 5 * ScoreBoard.y_interval,
                             DobasErtekelo.nagy_sor: ScoreBoard.start_y_coordinate + 6 * ScoreBoard.y_interval,
                             DobasErtekelo.kis_poker: ScoreBoard.start_y_coordinate + 7 * ScoreBoard.y_interval,
                             DobasErtekelo.nagy_poker: ScoreBoard.start_y_coordinate + 8 * ScoreBoard.y_interval
                             }


    def reset_calculated_score(self):

        for key in self.player_calculated_scores.key():
            self.player_calculated_scores[key] = None

    def draw_scoreboard(self):

        for func, text in self.player_scores.items():
            if text is not None:
                self.screen.blit(text, (self.player_column, self.y_coordinate[func]))

        for func, text in self.player_calculated_scores.items():
            if text is not None:
                self.screen.blit(text, (self.calculation_column, self.y_coordinate[func]))

        for func, text in self.cpu_scores.items():
            if text is not None:
                ##print("This would be rendered: ", text)
                # pprint.pprint(self.cpu_scores)
                self.screen.blit(text, (self.cpu_column, self.y_coordinate[func]))

        self.screen.blit(font.render(str(self.player_score), True, FontColors.cream),
                         (self.player_column, self.player_score_pos_y))
        self.screen.blit(font.render(str(self.cpu_score), True, FontColors.cream),
                         (self.cpu_column, self.cpu_score_pos_y))

    def create_text(self, score: int, func: Callable, score_type: ScoreType) -> None:

        text = font.render(str(score), True, FontColors.cream)

        print("This function was chosen", func, " and score ", score)

        match score_type:
            case ScoreType.PLAYER_SCORE:
                self.player_scores[func] = text
                self.player_score += score
            case ScoreType.CALCULATED_SCORE:
                self.player_calculated_scores[func] = text
            case ScoreType.CPU_SCORE:
                self.cpu_scores[func] = text
                self.cpu_score += score
