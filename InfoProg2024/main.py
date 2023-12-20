import random
import collections
from dataclasses import dataclass, field
from typing import List
import logging

logging.basicConfig(level=logging.DEBUG)


def random_dobas() -> List[int]:
    DOBASOK_SZAMA = 5
    return sorted([random.randint(1, 6) for _ in range(DOBASOK_SZAMA)])


@dataclass
class DobasData:
    dobas_sor: List[int] = field(default_factory=random_dobas)

    def __post_init__(self):
        self.counter_1 = collections.Counter(self.dobas_sor)
        self.counter_2 = collections.Counter(self.counter_1.values())


class DobasErtekelo:
    @staticmethod
    def nagy_sor(dobas_data: DobasData) -> int:
        return 20 if dobas_data.dobas_sor == [2, 3, 4, 5, 6] else 0

    @staticmethod
    def kis_sor(dobas_data: DobasData) -> int:
        return 15 if dobas_data.dobas_sor == [1, 2, 3, 4, 5] else 0

    @staticmethod
    def nagy_poker(dobas_data: DobasData) -> int:
        return 50 if max(dobas_data.counter_1.values()) == 5 else 0

    @staticmethod
    def full(dobas_data: DobasData) -> int:
        return sum(dobas_data.dobas_sor) if dobas_data.counter_2 == {2: 1, 3: 1} else 0

    @staticmethod
    def kis_poker(dobas_data: DobasData) -> int:
        leggyakoribb_szam = max(dobas_data.counter_1, key=dobas_data.counter_1.get)
        return 4 * leggyakoribb_szam if dobas_data.counter_1[leggyakoribb_szam] == 4 else 0

    @staticmethod
    def tetszoleges_kombinacio(dobas_data: DobasData) -> int:
        return sum(dobas_data.dobas_sor)

    @staticmethod
    def par(dobas_data: DobasData) -> int:
        parok = list(filter(lambda elem: elem[1] == 2, dobas_data.counter_1.items()))

        if len(parok) == 0:
            return 0

        return 2 * max(parok)[0]

    @staticmethod
    def drill(dobas_data: DobasData) -> int:
        harmasok = list(filter(lambda elem: elem[1] == 2, dobas_data.counter_1.items()))

        if len(harmasok) == 0:
            return 0

        return 3 * max(harmasok)[0]

    @staticmethod
    def ket_par(dobas_data: DobasData) -> int:
        if dobas_data.counter_2[2] != 2:
            return 0

        parok = list(filter(lambda elem: elem[1] == 2, dobas_data.counter_1.items()))

        return 2 * sum(i for i, _ in parok)


def ertekelesek_futtatasa(dobas_data: DobasData, ertekelo_set: set):
    """
    HARDMODE
    :param dobas_data:
    :param ertekelo_set:
    :return:
    """

    pontok = []

    for func in ertekelo_set:
        ertekeles = func(dobas_data)
        pontok.append(tuple([ertekeles, func]))

    return pontok


if __name__ == "__main__":
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
