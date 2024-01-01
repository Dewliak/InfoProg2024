import pytest

from InfoProg2024.modulok.dobas_modul.dobas_ertekelo import DobasData, DobasErtekelo


@pytest.mark.parametrize("dobas_data, varhato_ertek", [
    (DobasData([2, 3, 4, 5, 6]), 20),
    (DobasData([3, 4, 2, 6, 5]), 20),
    (DobasData([6, 5, 4, 3, 2]), 20),
    (DobasData([2, 3, 4, 5, 5]), 0),
    (DobasData([1, 2, 3, 4, 5]), 0),
    (DobasData([5, 5, 5, 5, 5]), 0),
    (DobasData([2, 3, 4, 5, 5]), 0),
    (DobasData([3, 4, 6, 5, 6]), 0),
])
def test_nagy_sor(dobas_data: DobasData, varhato_ertek: int):
    assert DobasErtekelo.nagy_sor(dobas_data) == varhato_ertek


@pytest.mark.parametrize("dobas_data, varhato_ertek", [
    (DobasData([1, 2, 3, 4, 5]), 15),
    (DobasData([2, 3, 4, 5, 6]), 0),
    (DobasData([1, 1, 1, 1, 1]), 0),
    (DobasData([1, 2, 3, 4, 1]), 0),
])
def test_kis_sor(dobas_data: DobasData, varhato_ertek: int):
    assert DobasErtekelo.kis_sor(dobas_data) == varhato_ertek


@pytest.mark.parametrize("dobas_data, varhato_ertek", [
    (DobasData([1, 1, 1, 1, 1]), 50),
    (DobasData([5, 5, 5, 5, 5]), 50),
    (DobasData([1, 2, 3, 4, 5]), 0),
    (DobasData([1, 2, 1, 2, 1]), 0),
    (DobasData([2, 2, 2, 3, 3]), 0),
    (DobasData([1, 1, 1, 3, 1]), 0),
])
def test_nagy_poker(dobas_data: DobasData, varhato_ertek: int):
    assert DobasErtekelo.nagy_poker(dobas_data) == varhato_ertek


@pytest.mark.parametrize("dobas_data, varhato_ertek", [
    (DobasData([1, 1, 1, 2, 2]), 7),
    (DobasData([2, 1, 1, 2, 2]), 8),
    (DobasData([1, 1, 1, 1, 2]), 0),
    (DobasData([1, 1, 1, 1, 1]), 0),
    (DobasData([1, 1, 1, 1, 1]), 0),
])
def test_full(dobas_data: DobasData, varhato_ertek: int):
    assert DobasErtekelo.full(dobas_data) == varhato_ertek


@pytest.mark.parametrize("dobas_data, varhato_ertek", [
    (DobasData([1, 1, 1, 1, 5]), 4),
    (DobasData([2, 2, 2, 2, 3]), 8),
    (DobasData([4, 4, 2, 4, 4]), 16),
    (DobasData([3, 3, 3, 3, 3]), 12),
    (DobasData([1, 2, 3, 4, 5]), 0),
    (DobasData([2, 2, 3, 3, 5]), 0),
    (DobasData([1, 3, 1, 3, 1]), 0),
    (DobasData([1, 5, 5, 1, 5]), 0),
    (DobasData([1, 1, 1, 1, 1]), 4),
])
def test_kis_poker(dobas_data: DobasData, varhato_ertek: int):
    assert DobasErtekelo.kis_poker(dobas_data) == varhato_ertek


@pytest.mark.parametrize('dobas_data, varhato_ertek', [
    (DobasData([1, 2, 3, 4, 5]), 15),
    (DobasData([5, 5, 5, 5, 5]), 25),
    (DobasData([1, 1, 3, 2, 5]), 12),
    (DobasData([1, 2, 5, 3, 5]), 16),
])
def test_tetszoleges_kombinacio(dobas_data: DobasData, varhato_ertek: int):
    assert DobasErtekelo.tetszoleges_kombinacio(dobas_data) == varhato_ertek


@pytest.mark.parametrize('dobas_data, varhato_ertek', [
    (DobasData([2, 2, 3, 4, 5]), 4),
    (DobasData([2, 2, 4, 4, 5]), 8),
    (DobasData([4, 2, 4, 4, 2]), 8),
    (DobasData([2, 2, 6, 4, 6]), 12),
    (DobasData([1, 3, 2, 4, 5]), 0),
    (DobasData([2, 6, 4, 6, 6]), 12),
    (DobasData([2, 2, 2, 2, 2]), 4),
])
def test_par(dobas_data: DobasData, varhato_ertek: int):
    assert DobasErtekelo.par(dobas_data) == varhato_ertek


@pytest.mark.parametrize('dobas_data, varhato_ertek', [
    (DobasData([2, 2, 2, 4, 5]), 6),
    (DobasData([2, 2, 2, 2, 5]), 6),
    (DobasData([2, 2, 3, 3, 3]), 9),
    (DobasData([2, 2, 2, 2, 2]), 6),
    (DobasData([1, 2, 3, 4, 5]), 0),
    (DobasData([5, 4, 6, 4, 6]), 0),
])
def test_drill(dobas_data: DobasData, varhato_ertek: int):
    assert DobasErtekelo.drill(dobas_data) == varhato_ertek


@pytest.mark.parametrize('dobas_data, varhato_ertek', [
    (DobasData([1, 1, 2, 3, 2]), 6),
    (DobasData([1, 1, 2, 1, 2]), 6),
    (DobasData([1, 1, 1, 1, 2]), 0),
    (DobasData([1, 1, 5, 5, 5]), 12),
    (DobasData([1, 1, 1, 1, 1]), 0),
    (DobasData([2, 3, 4, 5, 6]), 0),
])
def test_ket_par(dobas_data: DobasData, varhato_ertek: int):
    assert DobasErtekelo.ket_par(dobas_data) == varhato_ertek
