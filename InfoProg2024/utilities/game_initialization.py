from InfoProg2024.modulok.kocka import Dice, DiceImages,DEFAULT_ROLLING_LENGTH, DEFUALT_ROLLING_INTERVAL

from .settings.dice_settings import START_X, FIRST_ROW_Y, DISTANCE_BETWEEN_DICES, SECOND_ROW_Y
def init_dices():
    dice_images = DiceImages()

    CPU_dice1 = Dice(x=START_X,
                     y=FIRST_ROW_Y,
                     dice_image=dice_images,
                     rolling_images_limit=DEFAULT_ROLLING_LENGTH + DEFUALT_ROLLING_INTERVAL)
    CPU_dice2 = Dice(x=START_X + DISTANCE_BETWEEN_DICES,
                     y=FIRST_ROW_Y,
                     dice_image=dice_images,
                     rolling_images_limit=DEFAULT_ROLLING_LENGTH + 2 * DEFUALT_ROLLING_INTERVAL)
    CPU_dice3 = Dice(x=START_X + 2 * DISTANCE_BETWEEN_DICES,
                     y=FIRST_ROW_Y,
                     dice_image=dice_images,
                     rolling_images_limit=DEFAULT_ROLLING_LENGTH + 3 * DEFUALT_ROLLING_INTERVAL)
    CPU_dice4 = Dice(x=START_X + 3 * DISTANCE_BETWEEN_DICES,
                     y=FIRST_ROW_Y,
                     dice_image=dice_images,
                     rolling_images_limit=DEFAULT_ROLLING_LENGTH + 4 * DEFUALT_ROLLING_INTERVAL)
    CPU_dice5 = Dice(x=START_X + 4 * DISTANCE_BETWEEN_DICES, y=FIRST_ROW_Y, dice_image=dice_images,
                     rolling_images_limit=DEFAULT_ROLLING_LENGTH + 5 * DEFUALT_ROLLING_INTERVAL)

    PLAYER_dice1 = Dice(x=START_X,
                        y=SECOND_ROW_Y,
                        dice_image=dice_images,
                        rolling_images_limit=DEFAULT_ROLLING_LENGTH + DEFUALT_ROLLING_INTERVAL)
    PLAYER_dice2 = Dice(x=START_X + 1 * DISTANCE_BETWEEN_DICES,
                        y=SECOND_ROW_Y,
                        dice_image=dice_images,
                        rolling_images_limit=DEFAULT_ROLLING_LENGTH + 2 * DEFUALT_ROLLING_INTERVAL)
    PLAYER_dice3 = Dice(x=START_X + 2 * DISTANCE_BETWEEN_DICES,
                        y=SECOND_ROW_Y,
                        dice_image=dice_images,
                        rolling_images_limit=DEFAULT_ROLLING_LENGTH + 3 * DEFUALT_ROLLING_INTERVAL)
    PLAYER_dice4 = Dice(x=START_X + 3 * DISTANCE_BETWEEN_DICES,
                        y=SECOND_ROW_Y,
                        dice_image=dice_images,
                        rolling_images_limit=DEFAULT_ROLLING_LENGTH + 4 * DEFUALT_ROLLING_INTERVAL)
    PLAYER_dice5 = Dice(x=START_X + 4 * DISTANCE_BETWEEN_DICES,
                        y=SECOND_ROW_Y,
                        dice_image=dice_images,
                        rolling_images_limit=DEFAULT_ROLLING_LENGTH + 5 * DEFUALT_ROLLING_INTERVAL)

    CPU_dices = [CPU_dice1, CPU_dice2, CPU_dice3, CPU_dice4, CPU_dice5]
    PLAYER_dices = [PLAYER_dice1, PLAYER_dice2, PLAYER_dice3, PLAYER_dice4, PLAYER_dice5]

    return CPU_dices, PLAYER_dices
