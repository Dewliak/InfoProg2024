import random
import collections
from dataclasses import dataclass, field
from typing import List, Final
import logging

logging.basicConfig(level=logging.DEBUG)

# Konstansok
DOBASOK_SZAMA: Final[int] = 5
KOCKA_OLDALAK_SZAMA: Final[int] = 6


def random_dobas() -> List[int]:

    return [random.randint(1, 6) for _ in range(DOBASOK_SZAMA)]


@dataclass
class DobasData:
    dobas_sor: List[int] = field(default_factory=random_dobas)

    def __post_init__(self) -> None:
        # check if all elements all integers int dobas_sor
        if not all((type(element) is int) for element in self.dobas_sor):
            raise Exception("Nem minden elem szám")

        if any((element > KOCKA_OLDALAK_SZAMA or element < 0) for element in self.dobas_sor):
            raise Exception("A kocka legalább egyik oldala nem megfelelő,"
                            "a 6 oldalú kocka 1-6 -ig vehet fel értékeket")

        if len(self.dobas_sor) > DOBASOK_SZAMA:
            raise Exception("Legfeljebb 5 dobás lehet")

        self.dobas_sor.sort()

        self.counter_1 = collections.Counter(self.dobas_sor)
        self.counter_2 = collections.Counter(self.counter_1.values())
