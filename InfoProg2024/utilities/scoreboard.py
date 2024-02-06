from .assets import font, FontColors

from typing import Callable
from enum import Enum

from InfoProg2024.modulok.dobas_modul.dobas_ertekelo import DobasErtekelo


class ScoreType(Enum):
    PLAYER_SCORE = 1
    CALCULATED_SCORE = 2
    CPU_SCORE = 3


class ScoreBoard:
    start_y_coordinate = 96
    y_interval = 47

    def __init__(self, screen):

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

    def load_data(self, dict):
        self.player_score = dict['player_score']
        for kv in dict['player_scores'].items():
            print(kv)
            self.player_scores[eval(f"DobasErtekelo.{kv[0]}")] = kv[1]
        #self.player_score = dict(map(lambda kv: (eval(f"DobasErtekelo.{kv[0]}"),kv[1]),dict['player_scores'].items()))
        #self.player_scores = dict(map(lambda kv: (eval(f"DobasErtekelo.{kv[0]}"), kv[1]), dict["player_scores"].items()))
        self.cpu_score = dict['cpu_score']
        for kv in dict['cpu_scores'].items():
            self.cpu_scores[eval(f"DobasErtekelo.{kv[0]}")] = kv[1]
        for kv in dict['calculated_scores'].items():
            self.player_calculated_scores[eval(f"DobasErtekelo.{kv[0]}")] = kv[1]

    def get_data_to_save(self):

        data = {
            'player_score': self.player_score,
            'player_scores': dict(map(lambda kv: (kv[0].__name__, kv[1]), self.player_scores.items())),
            'cpu_score': self.cpu_score,
            'cpu_scores': dict(map(lambda kv: (kv[0].__name__, kv[1]), self.cpu_scores.items())),
            'calculated_scores': dict(map(lambda kv: (kv[0].__name__, kv[1]), self.player_calculated_scores.items()))
        }

        return data

    def reset_calculated_score(self):

        for key in self.player_calculated_scores.keys():
            self.player_calculated_scores[key] = None

    def draw_scoreboard(self):

        for func, text in self.player_scores.items():
            if text is not None:
                t = font.render(text, True, FontColors.cream)
                self.screen.blit(t, (self.player_column, self.y_coordinate[func]))

        for func, text in self.player_calculated_scores.items():
            if text is not None:
                t = font.render(text, True, FontColors.cream)
                self.screen.blit(t, (self.calculation_column, self.y_coordinate[func]))

        for func, text in self.cpu_scores.items():
            if text is not None:
                ##print("This would be rendered: ", text)
                # pprint.pprint(self.cpu_scores)
                t = font.render(text, True, FontColors.cream)
                self.screen.blit(t, (self.cpu_column, self.y_coordinate[func]))

        self.screen.blit(font.render(str(self.player_score), True, FontColors.cream),
                         (self.player_column, self.player_score_pos_y))
        self.screen.blit(font.render(str(self.cpu_score), True, FontColors.cream),
                         (self.cpu_column, self.cpu_score_pos_y))

    def create_text(self, score: int, func: Callable, score_type: ScoreType) -> None:

        text = font.render(str(score), True, FontColors.cream)

        #ALTERNATIVE METHOD NOT STORING OBJECTS, but tuples
        text = str(score)
        print("This function was chosen", func, " and score ", score)

        match score_type:
            case ScoreType.PLAYER_SCORE:
                self.player_scores[func] = str(score)
                self.player_score += score
            case ScoreType.CALCULATED_SCORE:
                self.player_calculated_scores[func] = text
            case ScoreType.CPU_SCORE:
                self.cpu_scores[func] = text
                self.cpu_score += score

    def reset(self):
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

        self.player_score = 0
        self.cpu_score = 0