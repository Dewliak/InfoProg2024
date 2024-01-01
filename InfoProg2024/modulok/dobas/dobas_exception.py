class DobasElementTypeException(Exception):
    """Akkor hasznaljuk, ha valamelyik elem, nem szám a dobás sorozatban"""
    def __init__(self):
        self.message = "Nem minden elem típusa szám a dobás sorozatban"
        super().__init__(self.message)


class DobasIntegerLimitException(Exception):
    """Akkor hasznaljuk, ha valamelyik elem, kisebb mint 1 vagy nagyobb mint az oldalak szama"""
    def __init__(self, kocka_oldalak_szama):
        self.message = f"Valamelyik elem kisebb mint 1, vagy meghaladja az oldalak számát({kocka_oldalak_szama})"
        super().__init__(self.message)


class DobasCountException(Exception):
    """Akkor hasznaljuk, ha a dobasok szama nem egyezik meg a megadottal"""
    def __init__(self, dobasok_szama):
        self.message = f"A dobasok szama nem egyezik meg a megadottal({dobasok_szama})"
        super().__init__(self.message)
