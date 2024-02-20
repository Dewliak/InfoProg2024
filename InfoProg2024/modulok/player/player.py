from typing import List, Tuple, Callable

from .player_entity import PlayerEntity, ALAP_DOBAS
from ..dobas_modul import DobasData


class Player(PlayerEntity):
    """
    Az osztály a játékost reprezentája.
    """
    def __init__(self):
        super().__init__()

        self.kiszamolt_pontok = None



    def reset(self) -> None:
        """
        Alaphelyzetbe rakja a változókat

        """
        self.kiszamolt_pontok = 0
        self.hasznalt_kombinaciok = [False for _ in range(len(self.kombinaciok))]
        self.maradek_jatek = len(self.kombinaciok)
        self.pont_lista = []
        self.pontok = 0
        self.dobas = ALAP_DOBAS

        for i, d in enumerate(self.dice_entities):
            self.dice_entities[i].set_dice_value(self.dobas.get_next())
            self.dice_entities[i].set_image()

    def load_data(self, dictionary):
        self.is_cpu = dictionary['is_cpu']
        self.maradek_jatek = dictionary['maradek_jatek']
        #TODO: dicto to dobas
        self.dobas = None if dictionary['dobas'] is None else DobasData(dictionary['dobas']['dobas_sor'])
        self.pont_lista = []
        if dictionary['pont_lista'] != []:
            for kv in dictionary['pont_lista']:
                #  Stringből csinálom DobasErtekelo objektumot
                self.pont_lista.append(tuple([kv[0], eval(f"DobasErtekelo.{kv[1]}")]))
        self.hasznalt_kombinaciok = dictionary['hasznalt_kombinaciok']

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
