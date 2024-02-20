from InfoProg2024.utilities.gui_controller import GUIController
from InfoProg2024.utilities import assets
from InfoProg2024.utilities.states import GameStates

from InfoProg2024.utilities.game_state_modules.calculate_point import calculate_point


def throw_state(control: GUIController):
    """
    Dobás állapota, szimulálja a dobásokat és lefut a dobás animáció
    """
    for d in control.game_controller.inactive.dice_entities:
        control.game_screen.blit(d.value_image, (d.x, d.y))

    if control.GAME_STATE == GameStates.DICE_THROW and control.game_controller.active.player_roll is False:
        # a player_roll az vizsgálja, hogy el vannak-e dobva a kockák

        control.game_controller.active.uj_dobas()

        assets.rolling_aud.play()

        control.game_controller.active.player_roll = True

        for i, d in enumerate(control.game_controller.active.dice_entities):
            control.game_controller.active.dice_entities[i].is_rolling = True

            control.game_controller.active.dice_entities[i].set_dice_value(
                control.game_controller.active.dobas.get_next())

            control.game_controller.active.dice_entities[i].set_image()

            # Dobás animáció
            control.game_screen.blit(control.game_controller.active.dice_entities[i].rolling_animation_image(),
                                     (d.x, d.y))
            control.game_controller.active.dice_entities[i].rolling_images_counter += 1

    else:
        if control.game_controller.active.player_roll:

            for i, d in enumerate(control.game_controller.active.dice_entities):

                if not d.is_rolling:
                    control.game_screen.blit(d.value_image, (d.x, d.y))  # rendereli a kockákat
                    continue

                control.game_screen.blit(control.game_controller.active.dice_entities[i].rolling_animation_image(),
                                         (d.x, d.y))

                control.game_controller.active.dice_entities[i].rolling_images_counter += 1

                if d.rolling_images_counter >= d.rolling_images_limit:
                    control.game_controller.active.dice_entities[i].is_rolling = False
                    control.game_controller.active.dice_entities[i].rolling_images_counter = 0

                    assets.rolling_stop_aud.play()

            if all(not x.is_rolling for x in
                   control.game_controller.active.dice_entities):  # ha már az egyik kocka sem pereg
                control.GAME_STATE = GameStates.SCORING

                calculate_point(control)
                control.game_controller.active.player_roll = False
        else:
            for d in control.game_controller.active.dice_entities:
                control.game_screen.blit(d.value_image, (d.x, d.y))

        if not control.game_controller.active.player_roll:  # ha nem pörögnek a kockák, akkor csak a kockákat renderelje
            for d in control.game_controller.active.dice_entities:
                control.game_screen.blit(d.value_image, (d.x, d.y))
