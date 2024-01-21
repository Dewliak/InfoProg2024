from typing import List, Tuple, Callable

from .player_entity import PlayerEntity
from ..dobas_modul import DobasData


class Player(PlayerEntity):
    def __init__(self):
         super().__init__()

         self.kiszamolt_pontok = None

    def ertekelesek_futtatasa(self) -> List[Tuple[int, Callable]]:

        pontok: List[Tuple[int, Callable]] = []

        for i,func in enumerate(self.kombinaciok):
            if not self.hasznalt_kombinaciok[i]:
                ertekeles: int = func(self.dobas)
                pontok.append(tuple([ertekeles, func]))

        self.kiszamolt_pontok = dict(map(lambda x: (x[1], x[0]), pontok))

        return pontok


    def play_hand_player(self, dobas_data):
        # TODO: player hand
        assert "Not implemented"
