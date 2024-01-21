from typing import Tuple, Callable, List

from .player_entity import PlayerEntity

class CPU(PlayerEntity):
    def __init__(self, hard_mode = False):
        super().__init__()

        self.hard_mode = hard_mode
        self.is_cpu = True
        self.szabad_kombinaciok: set = set(self.kombinaciok)

        self.maradek_jatek: int = len(self.kombinaciok)

    def reset(self):
        self.maradek_jatek: int = len(self.kombinaciok)
        self.szabad_kombinaciok: set = set(self.kombinaciok)

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

        #logging.debug(pontok)
        #pprint.pprint(pontok)
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
        self.pontok += self.pont_lista.append(tuple[0, self.kombinaciok[elso_szabalyos_hely_index]])
        self.hasznalt_kombinaciok[elso_szabalyos_hely_index] = True

        return tuple[0, self.kombinaciok[elso_szabalyos_hely_index]]
