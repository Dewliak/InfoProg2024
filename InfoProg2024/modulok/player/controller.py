from .player import Player
from .cpu import CPU


from typing import Union

class Controller:
    def __init__(self, player: Player, cpu: CPU):
        self.player: Player = player
        self.cpu: CPU = cpu

        self.player_turn = True

        self.active: Union[Player, CPU] = self.player
        self.inactive: Union[Player, CPU] = self.cpu

    def change_active_player(self):
        self.player_turn = not self.player_turn

        self.active, self.inactive = self.inactive, self.active
