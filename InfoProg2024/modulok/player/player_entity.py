from typing import List, Tuple, Callable

from InfoProg2024.modulok.dobas_modul import DobasData, DobasErtekelo


class PlayerEntity:
    def __init__(self):

        self.dobas = None
        self.player_roll = False
        self.pontok: int = 0
        self.pont_lista: List[Tuple[int, Callable]] = []

        self.kombinaciok: List[Callable] = [DobasErtekelo.tetszoleges_kombinacio, DobasErtekelo.par,
                                            DobasErtekelo.drill,DobasErtekelo.ket_par,
                                            DobasErtekelo.kis_poker, DobasErtekelo.full,
                                            DobasErtekelo.kis_sor, DobasErtekelo.nagy_sor, DobasErtekelo.nagy_poker]

        self.hasznalt_kombinaciok: List[bool] = [False for _ in range(len(self.kombinaciok))]

        self.dice_entities = []

    def uj_dobas(self):
        self.dobas = DobasData()

    def ertekelesek_futtatasa(self, dobas_data: DobasData, ertekelo_set: set) -> List[Tuple[int, Callable]]:
        """
        HARDMODE
        :param dobas_data:
        :param ertekelo_set:
        :return:
        """

        kocka_pontok: List[Tuple[int, Callable]] = []

        for func in ertekelo_set:
            ertekeles: int = func(dobas_data)
            kocka_pontok.append(tuple([ertekeles, func]))

        return kocka_pontok
