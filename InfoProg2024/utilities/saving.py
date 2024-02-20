import json
import pprint


def save_game(controller, scoreboard) -> None:
    """
    Elmenti a játékot JSON formában
    """
    data = {'controller': controller.get_data_to_save(),
            'scoreboard': scoreboard.get_data_to_save()}
    pprint.pprint(data)
    with open("saving.json", "w") as f:
        json.dump(data, f)

