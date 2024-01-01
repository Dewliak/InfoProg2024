import random
import collections
from dataclasses import dataclass, field
from typing import List, Final
import logging

from InfoProg2024.modulok.dobas.dobas_exception import (
    DobasElementTypeException,
    DobasCountException,
    DobasIntegerLimitException)

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
            raise DobasElementTypeException

        if any((element > KOCKA_OLDALAK_SZAMA or element < 0) for element in self.dobas_sor):
            raise DobasIntegerLimitException(KOCKA_OLDALAK_SZAMA)

        if len(self.dobas_sor) != DOBASOK_SZAMA:
            raise DobasCountException(DOBASOK_SZAMA)

        self.dobas_sor.sort()

        self.counter_1 = collections.Counter(self.dobas_sor)
        self.counter_2 = collections.Counter(self.counter_1.values())
