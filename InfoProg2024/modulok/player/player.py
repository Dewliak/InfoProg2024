from typing import List, Tuple, Callable

from InfoProg2024.modulok.dobas_modul.dobas import DobasData

from .player_entity import PlayerEntity
from ..dobas_modul import DobasData


class Player(PlayerEntity):
    def __init__(self):
         super().__init__()

         self.kiszamolt_pontok = None



    def reset(self):
        self.kiszamolt_pontok = 0
        self.hasznalt_kombinaciok = [False for _ in range(len(self.kombinaciok))]
        self.maradek_jatek = len(self.kombinaciok)
        self.pont_lista = []
        self.pontok = 0
        self.dobas = DobasData([1, 1, 1, 1, 1])

        for i, d in enumerate(self.dice_entities):
            self.dice_entities[i].set_dice_value(self.dobas.get_next())
            self.dice_entities[i].set_image()

    def load_data(self,dict):
        self.is_cpu = dict['is_cpu']
        self.maradek_jatek = dict['maradek_jatek']
        #TODO: dicto to dobas
        self.dobas = None if dict['dobas'] is None else DobasData(dict['dobas']['dobas_sor'])
        self.pont_lista = []
        if dict['pont_lista'] != []:
            for kv in dict['pont_lista']:
                self.pont_lista.append(tuple([kv[0], eval(f"DobasErtekelo.{kv[1]}")]))
        self.hasznalt_kombinaciok = dict['hasznalt_kombinaciok']
    def get_data_to_save(self) -> dict:
        print(self.pont_lista)
        data = {"is_cpu": self.is_cpu,
                "maradek_jatek": self.maradek_jatek,
                "dobas": None if self.dobas is None else self.dobas.as_dict(),
                "pont_lista":  list(map(lambda kv: tuple([kv[0], kv[1].__name__]),self.pont_lista)),
                "hasznalt_kombinaciok": self.hasznalt_kombinaciok,
                }

        return data

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
