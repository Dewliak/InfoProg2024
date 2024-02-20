from typing import Tuple, Callable, List

from InfoProg2024.modulok.dobas_modul.dobas import DobasData
from InfoProg2024.modulok.dobas_modul.dobas_ertekelo import DobasErtekelo
from .player_entity import PlayerEntity, ALAP_DOBAS


class CPU(PlayerEntity):
    """
    A CPU osztály, a gép objektumát hozza létre.
    """
    def __init__(self, hard_mode=False):
        super().__init__()

        self.hard_mode = hard_mode
        self.is_cpu = True
        self.szabad_kombinaciok: set = set(self.kombinaciok)

        self.maradek_jatek: int = len(self.kombinaciok)

    def reset(self) -> None:
        """
        Alap állapotba rakja az objektumot
        """
        self.maradek_jatek: int = len(self.kombinaciok)
        self.szabad_kombinaciok: set = set(self.kombinaciok)
        self.hasznalt_kombinaciok = [False for _ in range(len(self.kombinaciok))]

        self.pontok = 0
        self.pont_lista = []
        self.dobas = ALAP_DOBAS

        for i, d in enumerate(self.dice_entities):
            self.dice_entities[i].set_dice_value(self.dobas.get_next())
            self.dice_entities[i].set_image()

    def load_data(self, dictionary) -> None:
        """
        Feldolgozza a beolvasott adatokat
        :param dictionary: JSON data, amit szótár formára alakítottunk
        """

        self.hard_mode = dictionary['hard_mode']
        self.is_cpu = dictionary['is_cpu']
        self.maradek_jatek = dictionary['maradek_jatek']
        self.dobas = None if dictionary['dobas'] is None else DobasData(dictionary['dobas']['dobas_sor'])
        self.pont_lista = []

        if dictionary['pont_lista'] != []:
            for kv in dictionary['pont_lista']:
                self.pont_lista.append(tuple([kv[0], eval(f"DobasErtekelo.{kv[1]}")]))

        self.hasznalt_kombinaciok = dictionary["hasznalt_kombinaciok"]
        self.szabad_kombinaciok = list(map(lambda x: eval(f"DobasErtekelo.{x}"),dictionary['szabad_kombinaciok']))

    def get_data_to_save(self) -> dict:
        """
        Előkészíti a változókat a mentéshez
        """

        data = {"hard_mode": self.hard_mode,
                "is_cpu": self.is_cpu,
                "maradek_jatek": self.maradek_jatek,
                "dobas": None if self.dobas is None else self.dobas.as_dict(),
                "pont_lista": list(map(lambda kv: tuple([kv[0], kv[1].__name__]),self.pont_lista)),
                "hasznalt_kombinaciok": self.hasznalt_kombinaciok,
                "szabad_kombinaciok": list(map(lambda x: x.__name__,self.szabad_kombinaciok))}

        return data


    def play_hand(self):
        """
        Szimulálja azt, egy dobásnál kiválaszt egy helyet, ahova még nincsen pont írva a nehézségi fok alapján
        """
        if self.hard_mode:
            return self.play_hard()
        else:
            return self.play_easy()

    def set_hard_mode(self):
        """
        Nehézre rakja a nehézséget
        """
        self.hard_mode = True

    def set_easy_mode(self):
        """
        Könnyűre rakja a nehézséget
        """
        self.hard_mode = False

    def play_hard(self) -> Tuple[int, Callable]:
        pontok: List[Tuple[int, Callable]] = self.ertekelesek_futtatasa(self.dobas, self.szabad_kombinaciok)
        legtobb_pont: Tuple[int, Callable] = max(pontok, key=lambda x: x[0])

        self.szabad_kombinaciok.remove(legtobb_pont[1])

        self.pontok += legtobb_pont[0]
        self.pont_lista.append(legtobb_pont)

        return legtobb_pont

    def play_easy(self) -> Tuple[int, Callable]:
        # TODO: A problema, hogyha vegigmegyunk es mindenhol 0 van, akkor nem rakja bele az elsobe ahova lehert
        # TODO: Csinalni erre a problemara teszteket
        found: bool = False
        elso_szabalyos_hely_index: int = None

        for i in range(0, len(self.kombinaciok)):
            if not self.hasznalt_kombinaciok[i]:
                pont: int = self.kombinaciok[i](self.dobas)

                if pont != 0:
                    self.pontok += pont
                    self.pont_lista.append(tuple([pont, self.kombinaciok[i]]))
                    self.hasznalt_kombinaciok[i] = True

                    return tuple([pont, self.kombinaciok[i]])
                else:
                    if not found:
                        found = True
                        elso_szabalyos_hely_index = i

        # Ha ide jutunk, akkor nem találtunk olyan kombinaciot,
        # ami pontot adott volna, így az első szabad helyre tesszük
        self.pont_lista.append(tuple[0, self.kombinaciok[elso_szabalyos_hely_index]])
        self.hasznalt_kombinaciok[elso_szabalyos_hely_index] = True

        return tuple([0, self.kombinaciok[elso_szabalyos_hely_index]])
