import json


def debug_game_data(scoreboard, controller) -> None:
    scoreboard_attr = vars(scoreboard)
    cont_attr = vars(controller)
    player_attr = vars(controller.player)
    cpu_attr = vars(controller.cpu)

    json_data = {"scoreboard_data": dict(map(lambda x: (str(x[0]), str(x[1])), scoreboard_attr.items())),
                 "controller": dict(map(lambda x: (str(x[0]), str(x[1])), cont_attr.items())),
                 "player_data": dict(map(lambda x: (str(x[0]), str(x[1])), player_attr.items())),
                 "cpu_data": dict(map(lambda x: (str(x[0]), str(x[1])), cpu_attr.items()))}

    debug_save_path = "utilities/debug/debug.json"
    with open(debug_save_path, 'w') as f:
        json.dump(json_data, f)

    print("Debug data save to", debug_save_path)
