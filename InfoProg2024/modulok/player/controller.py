from .player import Player
from .cpu import CPU


from typing import Union


class Controller:
    """
    A különböző modulokat ez köti össze, ezen keresztül az osztályon keresztül
    tudnak kommunikálni egymással a modulok, valamint az alapvető változók találhatóak meg benne
    """
    def __init__(self, player: Player, cpu: CPU):
        self.player: Player = player  # Játékos objektuma
        self.cpu: CPU = cpu  # Gép objektuma

        self.player_name = "Player"  # Játékos neve
        self.player_turn = True

        self.active: Union[Player, CPU] = self.player
        self.inactive: Union[Player, CPU] = self.cpu

        self.high_score_save = False
        self.load_name_from_save = False

    def load_data(self, dictionary) -> None:
        """
        Játék adatainak beolvasása
        :param dictionary: JSON formátumban van elmentve, ezt szótárrá alakítjuk beolvasáskor
        """
        self.player_turn = dictionary["player_turn"]

        if self.load_name_from_save:
            self.player_name = dictionary['player_name']
        self.add_active_inactive()

        self.player.load_data(dictionary['player'])
        self.cpu.load_data(dictionary['cpu'])

    def get_data_to_save(self) -> dict:
        """
        Előkészíti az adatokat a mentéshez
        :return:
        """
        data: dict = {
            'player_turn': self.player_turn,
            'player_name': self.player_name,
            'player': self.player.get_data_to_save(),
            'cpu': self.cpu.get_data_to_save(),

        }

        return data

    def add_active_inactive(self) -> None:
        """
        Betöltés után aktiválja a megfelelő játékost
        """
        if self.player_turn:
            self.active = self.player
            self.inactive = self.cpu
        else:
            self.active = self.cpu
            self.inactive = self.player

    def change_active_player(self) -> None:
        """
        Kicseréli az aktív játékost játékos -> gép vagy gép -> játékos
        """
        self.player_turn = False if self.player_turn else True

        self.active, self.inactive = self.inactive, self.active

    def reset(self) -> None:
        """
        A játék újraindítása, minden alap beállításba kerül
        """
        self.cpu.reset()
        self.player.reset()
        self.active = self.player
        self.inactive = self.cpu

        self.high_score_save = False
