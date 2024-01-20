from typing import List, Tuple, Callable
import logging

from InfoProg2024.modulok.dobas_modul import DobasData, DobasErtekelo
import pprint
logging.basicConfig(level=logging.DEBUG)






if __name__ == "__main__":

    #player = Player()
    #easy_cpu = CPU(hard_mode= False)
    hard_cpu = CPU(hard_mode= True)

    for _ in range(9):
        hard_cpu.uj_dobas()
        hard_cpu.play_hand()

