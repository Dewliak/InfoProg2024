import pytest

from typing import List

from InfoProg2024.modulok.dobas_modul import DobasData
from InfoProg2024.modulok.dobas_modul import dobas_exceptions


def test_dobas_element_type():
    with pytest.raises(dobas_exceptions.DobasElementTypeException):
        DobasData([1, 2, "3", "4", 5])


@pytest.mark.parametrize("dobas_sor", [
    [1, 2, 3, 4],
    [2, 3, 4, 5, 6, 4]
])
def test_dobas_size(dobas_sor: List[int]):
    with pytest.raises(dobas_exceptions.DobasCountException):
        DobasData(dobas_sor)


def test_dobas_integer_limit():
    with pytest.raises(dobas_exceptions.DobasIntegerLimitException):
        DobasData([2, 3, 4, 5, 7])
