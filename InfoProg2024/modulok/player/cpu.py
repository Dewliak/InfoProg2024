from typing import Tuple, Callable, List

from InfoProg2024.modulok.dobas_modul.dobas import DobasData
from InfoProg2024.modulok.dobas_modul.dobas_ertekelo import DobasErtekelo
from .player_entity import PlayerEntity


class CPU(PlayerEntity):
    def __init__(self, hard_mode=False):
        super().__init__()

        self.hard_mode = hard_mode
        self.is_cpu = True
        self.szabad_kombinaciok: set = set(self.kombinaciok)

        self.maradek_jatek: int = len(self.kombinaciok)

    def reset(self):
        self.maradek_jatek: int = len(self.kombinaciok)
        self.szabad_kombinaciok: set = set(self.kombinaciok)
        self.hasznalt_kombinaciok = [False for _ in range(len(self.kombinaciok))]

        self.pontok = 0
        self.pont_lista = []
        self.dobas = DobasData([1,1,1,1,1])

        for i, d in enumerate(self.dice_entities):
            self.dice_entities[i].set_dice_value(self.dobas.get_next())
            self.dice_entities[i].set_image()

    def load_data(self,dict):

        self.hard_mode = dict['hard_mode']
        self.is_cpu = dict['is_cpu']
        self.maradek_jatek = dict['maradek_jatek']
        self.dobas = None if dict['dobas'] is None else DobasData(dict['dobas']['dobas_sor'])
        self.pont_lista = []
        if dict['pont_lista'] != []:
            for kv in dict['pont_lista']:
                self.pont_lista.append(tuple([kv[0], eval(f"DobasErtekelo.{kv[1]}")]))


            #self.pont_lista = list(map(lambda kv: tuple([kv[0], eval(f"DobasErtekelo.{kv[1]}")]),dict['pont_lista'])),
        self.hasznalt_kombinaciok = dict["hasznalt_kombinaciok"]
        self.szabad_kombinaciok = list(map(lambda x: eval(f"DobasErtekelo.{x}"),dict['szabad_kombinaciok']))

        print("TYPE AFTER LOAD", type(self.pont_lista))
    def get_data_to_save(self) -> dict:
        print("CPU point list", type(self.pont_lista))
        data = {"hard_mode": self.hard_mode,
                "is_cpu": self.is_cpu,
                "maradek_jatek": self.maradek_jatek,
                "dobas": None if self.dobas is None else self.dobas.as_dict(),
                "pont_lista": list(map(lambda kv: tuple([kv[0], kv[1].__name__]),self.pont_lista)),
                "hasznalt_kombinaciok": self.hasznalt_kombinaciok,
                "szabad_kombinaciok": list(map(lambda x: x.__name__,self.szabad_kombinaciok))}

        return data


    def play_hand(self):
        if self.hard_mode:
            return self.play_hard()
        else:
            return self.play_easy()

    def set_hard_mode(self):
        self.hard_mode = True

    def set_easy_mode(self):
        self.hard_mode = False

    def play_hard(self) -> Tuple[int, Callable]:
        pontok: List[Tuple[int, Callable]] = self.ertekelesek_futtatasa(self.dobas, self.szabad_kombinaciok)
        legtobb_pont: Tuple[int, Callable] = max(pontok, key=lambda x: x[0])

        # logging.debug(pontok)
        # pprint.pprint(pontok)
        print(f"LEGTOBB PONTOS KITOROLVE: {legtobb_pont}")
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

    def play_very_easy(self) -> Tuple[int, Callable]:

        #TODO: implement this into the game
        for i in range(0, len(self.kombinaciok)):
            if not self.hasznalt_kombinaciok[i]:
                pont: int = self.kombinaciok[i](self.dobas)
                self.pont_lista.append(tuple([pont, self.kombinaciok[i]]))
                self.hasznalt_kombinaciok[i] = True

                return tuple([pont, self.kombinaciok[i]])

        return tuple([0, None])
