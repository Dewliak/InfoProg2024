""
class Player:
    def __init__(self, is_ai=True, hard_mode=False):
        self.hard_mode: bool = hard_mode
        self.is_ai: bool = is_ai
        self.pontok: int = 0
        self.pont_lista: List[Tuple[int, Callable]] = []

        self.kombinaciok: List[Callable] = [DobasErtekelo.tetszoleges_kombinacio, DobasErtekelo.par,
                                            DobasErtekelo.drill,DobasErtekelo.ket_par,
                                            DobasErtekelo.kis_poker, DobasErtekelo.full,
                                            DobasErtekelo.kis_sor, DobasErtekelo.nagy_sor, DobasErtekelo.nagy_poker]

        self.hasznalt_kombinaciok: List[bool] = [False for _ in range(len(self.kombinaciok))]

        if is_ai and hard_mode:
            self.szabad_kombinaciok: set = set(self.kombinaciok)

    def play_hand(self, dobas_data):

        if self.is_ai:
            self.play_hand_ai(dobas_data)
        else:
            self.play_hand_ai(dobas_data)

    def play_hand_ai(self, dobas_data) -> None:
        if self.hard_mode:
            pontok: Tuple[int, Callable] = self.ertekelesek_futtatasa(dobas, hardmode_func_set)
            legtobb_pont: Tuple[int, Callable] = max(pontok, key=lambda x: x[0])

            logging.debug(pontok)

            self.szabad_kombinaciok.remove(legtobb_pont[1])

            self.pontok += legtobb_pont[0]
            self.pont_lista.append(legtobb_pont)
        else:
            # TODO: A problema, hogyha vegigmegyunk es mindenhol 0 van, akkor nem rakja bele az elsobe ahova lehert
            found: bool = False
            elso_szabalyos_hely_index: int = None

            for i in range(0, len(self.kombinaciok)):
                if not self.hasznalt_kombinaciok[i]:
                    pont = self.kombinaciok[i](dobas)

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

    def play_hand_player(self, dobas_data):
        # TODO: player hand
        pass

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
"""




"""
HARDMODE: bool = True
points: int = 0
point_list: List[Tuple[int, Callable]] = []
hardmode_func_set = {
    DobasErtekelo.tetszoleges_kombinacio, DobasErtekelo.par, DobasErtekelo.drill,
    DobasErtekelo.ket_par, DobasErtekelo.kis_poker, DobasErtekelo.full,
    DobasErtekelo.kis_sor, DobasErtekelo.nagy_sor, DobasErtekelo.nagy_poker
}

easymode_func_list = [DobasErtekelo.tetszoleges_kombinacio, DobasErtekelo.par, DobasErtekelo.drill,
                      DobasErtekelo.ket_par, DobasErtekelo.kis_poker, DobasErtekelo.full,
                      DobasErtekelo.kis_sor, DobasErtekelo.nagy_sor, DobasErtekelo.nagy_poker]
easymode_func_list_used = [False for _ in range(len(easymode_func_list))]
print(type(hardmode_func_set))
print(type(easymode_func_list_used))

for _ in range(9):
    dobas = DobasData()

    if HARDMODE:
        pontok = self.ertekelesek_futtatasa(dobas, hardmode_func_set)
        logging.debug(pontok)
        legtobb_pont = max(pontok, key=lambda x: x[0])

        hardmode_func_set.remove(legtobb_pont[1])

        points += legtobb_pont[0]
        point_list.append(legtobb_pont)
    else:

        for i in range(0, len(easymode_func_list)):
            if not easymode_func_list_used[i]:
                pont = easymode_func_list[i](dobas)

                if pont != 0:
                    points += pont
                    point_list.append(tuple([pont, easymode_func_list[i]]))

                    easymode_func_list_used[i] = True

logging.debug(f"Points: {points}")
logging.debug(point_list)

"""
