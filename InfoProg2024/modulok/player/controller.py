from .player import Player
from .cpu import CPU


from typing import Union

class Controller:
    def __init__(self, player: Player, cpu: CPU):
        self.player: Player = player
        self.cpu: CPU = cpu

        self.player_name = "Player"
        self.player_turn = True

        self.active: Union[Player, CPU] = self.player
        self.inactive: Union[Player, CPU] = self.cpu

        self.high_score_save = False

        self.load_name_from_save = False

    def load_data(self, dict):
        self.player_turn = dict["player_turn"]

        if self.load_name_from_save:
            self.player_name = dict['player_name']
        self.add_active_inactive()

        self.player.load_data(dict['player'])
        self.cpu.load_data(dict['cpu'])

    def get_data_to_save(self):

        data = {
            'player_turn': self.player_turn,
            'player_name': self.player_name,
            'player': self.player.get_data_to_save(),
            'cpu': self.cpu.get_data_to_save(),

        }

        return data

    def add_active_inactive(self):

        if self.player_turn:
            self.active = self.player
            self.inactive = self.cpu
        else:
            self.active = self.cpu
            self.inactive = self.player


    def change_active_player(self):

        self.player_turn = False if self.player_turn else True

        self.active, self.inactive = self.inactive, self.active

    def reset(self):

        self.cpu.reset()
        self.player.reset()
        self.active = self.player
        self.inactive = self.cpu

        self.high_score_save = False

