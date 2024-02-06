import pprint
import json


def load_game(control):

    with open("saving.json", 'r') as f:
        data = json.load(f)

        control.game_controller.load_data(data['controller'])
        control.game_scoreboard.load_data(data['scoreboard'])

        print("PLAYER DOBAS", control.game_controller.player.dobas)

        for i in range(len(control.game_controller.active.dice_entities)):

            control.game_controller.active.dice_entities[i].set_dice_value(control.game_controller.active.dobas.get_next())
            control.game_controller.inactive.dice_entities[i].set_dice_value(control.game_controller.inactive.dobas.get_next())

            control.game_controller.active.dice_entities[i].set_image()
            control.game_controller.inactive.dice_entities[i].set_image()

        pprint.pprint(data)

