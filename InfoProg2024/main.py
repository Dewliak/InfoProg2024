from typing import List, Tuple, Callable
import logging

from InfoProg2024.modulok.dobas.dobas import DobasData
from InfoProg2024.modulok.dobas_ertekelo.dobas_ertekelo import DobasErtekelo

logging.basicConfig(level=logging.DEBUG)


def ertekelesek_futtatasa(dobas_data: DobasData, ertekelo_set: set) -> List[Tuple[int, Callable]]:
    """
    HARDMODE
    :param dobas_data:
    :param ertekelo_set:
    :return:
    """

    kocka_pontok: List[Tuple[int, Callable]] = []

    for func in ertekelo_set:
        ertekeles = func(dobas_data)
        kocka_pontok.append(tuple([ertekeles, func]))

    return kocka_pontok


if __name__ == "__main__":
    test = DobasData([1, "2", 3, 4, 5, 6, 7, 8, 9])
    print(test)

    HARDMODE = True
    points = 0
    point_list = []
    hardmode_func_set = {
        DobasErtekelo.tetszoleges_kombinacio, DobasErtekelo.par, DobasErtekelo.drill,
        DobasErtekelo.ket_par, DobasErtekelo.kis_poker, DobasErtekelo.full,
        DobasErtekelo.kis_sor, DobasErtekelo.nagy_sor, DobasErtekelo.nagy_poker
    }

    easymode_func_list = [DobasErtekelo.tetszoleges_kombinacio, DobasErtekelo.par, DobasErtekelo.drill,
                          DobasErtekelo.ket_par, DobasErtekelo.kis_poker, DobasErtekelo.full,
                          DobasErtekelo.kis_sor, DobasErtekelo.nagy_sor, DobasErtekelo.nagy_poker]
    easymode_func_list_used = [False for _ in range(len(easymode_func_list))]

    for _ in range(9):
        dobas = DobasData()

        if HARDMODE:
            pontok = ertekelesek_futtatasa(dobas, hardmode_func_set)
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
