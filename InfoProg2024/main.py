from typing import List, Tuple, Callable
import logging

from InfoProg2024.modulok.dobas_modul import DobasData, DobasErtekelo
import pprint
logging.basicConfig(level=logging.DEBUG)


class PlayerEntity:
    def __init__(self):

        self.dobas = None

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


class CPU(PlayerEntity):
    def __init__(self, hard_mode = False):
        super().__init__()

        self.hard_mode = hard_mode

        self.szabad_kombinaciok: set = set(self.kombinaciok)

    def play_hand(self):
        if self.hard_mode:
            self.play_hard()
        else:
            self.play_easy()

    def play_hard(self) -> None:
        pontok: Tuple[int, Callable] = self.ertekelesek_futtatasa(self.dobas, self.szabad_kombinaciok)
        legtobb_pont: Tuple[int, Callable] = max(pontok, key=lambda x: x[0])

        logging.debug(pontok)
        pprint.pprint(pontok)
        print(f"LEGTOBB PONTOS KITOROLVE: {legtobb_pont}")
        self.szabad_kombinaciok.remove(legtobb_pont[1])

        self.pontok += legtobb_pont[0]
        self.pont_lista.append(legtobb_pont)

    def play_easy(self) -> None:
        # TODO: A problema, hogyha vegigmegyunk es mindenhol 0 van, akkor nem rakja bele az elsobe ahova lehert
        # TODO: Csinalni erre a problemara teszteket
        found: bool = False
        elso_szabalyos_hely_index: int = None

        for i in range(0, len(self.kombinaciok)):
            if not self.hasznalt_kombinaciok[i]:
                pont = self.kombinaciok[i](self.dobas)

                if pont != 0:
                    self.pontok += pont
                    self.pont_lista.append(tuple([pont, self.kombinaciok[i]]))
                    self.hasznalt_kombinaciok[i] = True

                    return
                else:
                    if not found:
                        found = True
                        elso_szabalyos_hely_index = i

        # Ha ide jutunk, akkor nem találtunk olyan kombinaciot,
        # ami pontot adott volna, így az első szabad helyre tesszük
        self.pontok += self.pont_lista.append(tuple[0, self.kombinaciok[elso_szabalyos_hely_index]])
        self.hasznalt_kombinaciok[elso_szabalyos_hely_index] = True

        return

class Player(PlayerEntity):
    def __init__(self):
         super().__init__()

    def play_hand_player(self, dobas_data):
        # TODO: player hand
        assert "Not implemented"

if __name__ == "__main__":

    #player = Player()
    #easy_cpu = CPU(hard_mode= False)
    hard_cpu = CPU(hard_mode= True)

    for _ in range(9):
        hard_cpu.uj_dobas()
        hard_cpu.play_hand()

