import logging

from .dobas import DobasData

logger = logging.getLogger(__name__)


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
        return 4 * leggyakoribb_szam if dobas_data.counter_1[leggyakoribb_szam] >= 4 else 0

    @staticmethod
    def tetszoleges_kombinacio(dobas_data: DobasData) -> int:
        return sum(dobas_data.dobas_sor)

    @staticmethod
    def par(dobas_data: DobasData) -> int:
        parok = list(filter(lambda elem: elem[1] >= 2, dobas_data.counter_1.items()))

        if len(parok) == 0:
            return 0

        return 2 * max(parok)[0]

    @staticmethod
    def drill(dobas_data: DobasData) -> int:
        harmasok = list(filter(lambda elem: elem[1] >= 3, dobas_data.counter_1.items()))

        if len(harmasok) == 0:
            return 0

        return 3 * max(harmasok)[0]

    @staticmethod
    def ket_par(dobas_data: DobasData) -> int:
        #TODO EZ NEM BIZTOS HOGY MINDIG JO
        logging.debug(f"Parok: {dobas_data.counter_2}")
        if (dobas_data.counter_2[2] + dobas_data.counter_2[3]) != 2:
            return 0

        parok = list(filter(lambda elem: (2 <= elem[1] < 4), dobas_data.counter_1.items()))
        return 2 * sum(i for i, _ in parok)
