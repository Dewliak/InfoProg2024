import pprint
import json


def load_game(controller, scoreboard):

    with open("saving.json", 'r') as f:
        data = json.load(f)

        controller.load_data(data['controller'])
        scoreboard.load_data(data['scoreboard'])

        print("PLAYER DOBAS", controller.player.dobas)

        for i in range(len(controller.active.dice_entities)):

            controller.active.dice_entities[i].set_dice_value(controller.active.dobas.get_next())
            controller.inactive.dice_entities[i].set_dice_value(controller.inactive.dobas.get_next())

            controller.active.dice_entities[i].set_image()
            controller.inactive.dice_entities[i].set_image()

        pprint.pprint(data)

    return controller, scoreboard
