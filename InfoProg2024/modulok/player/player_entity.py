from typing import List, Tuple, Callable

from InfoProg2024.modulok.dobas_modul import DobasData, DobasErtekelo

ALAP_DOBAS = DobasData([1,1,1,1,1]) # Alapdobás, az első dobás előtti állapot
class PlayerEntity:
    """
    A PlayerEntity osztály a játékos és a cpu osztályok alapját képezi, olyan változók vannak itt,
    amelyet mindkét osztályban jelen
    """
    def __init__(self):

        self.dobas = ALAP_DOBAS
        self.player_roll = False
        self.pontok: int = 0
        self.is_cpu = False
        self.pont_lista: List[Tuple[int, Callable]] = []

        # Az összes szabályos kombináció
        self.kombinaciok: List[Callable] = [DobasErtekelo.tetszoleges_kombinacio, DobasErtekelo.par,
                                            DobasErtekelo.drill,DobasErtekelo.ket_par,
                                             DobasErtekelo.full, DobasErtekelo.kis_sor, DobasErtekelo.nagy_sor,
                                            DobasErtekelo.kis_poker, DobasErtekelo.nagy_poker]

        # Hány kör van még hátra
        self.maradek_jatek = len(self.kombinaciok)
        self.hasznalt_kombinaciok: List[bool] = [False for _ in range(len(self.kombinaciok))]

        # Maga a játék kockák vannak itt, azok az objektumok, amelyeket kirajzulunk a képernyőre
        self.dice_entities = []

    def reset(self) -> None:
        """
        Adatok nullázása
        """
        self.maradek_jatek = len(self.kombinaciok)
        self.hasznalt_kombinaciok = [False for _ in range(len(self.kombinaciok))]

    def uj_dobas(self) -> None:
        """
        Új dobást szimulál
        """
        self.dobas = DobasData()

    def ertekelesek_futtatasa(self, dobas_data: DobasData, ertekelo_set: set) -> List[Tuple[int, Callable]]:
        """
        Azokat a kombinációkat futtatja le és értékeli ki, amelyekhez még nincs pont rendelve
        :param dobas_data:
        :param ertekelo_set:
        :return:
        """

        kocka_pontok: List[Tuple[int, Callable]] = []

        for func in ertekelo_set:
            ertekeles: int = func(dobas_data)
            kocka_pontok.append(tuple([ertekeles, func]))

        return kocka_pontok
