from .player_entity import PlayerEntity
from .cpu import CPU
from .player import Player
from .controller import Controller

controller = Controller(Player(), CPU())