from .dice_images import DiceImages

DEFAULT_ROLLING_LENGTH = 8
DEFUALT_ROLLING_INTERVAL = 6


class Dice:
    def __init__(self, x: int, y: int, dice_image: DiceImages, rolling_images_limit=8):
        self.x: int = x
        self.y: int = y

        self.dice_image: DiceImages = dice_image

        self.number: int = 1
        self.is_rolling: bool = False

        self.rolling_images_counter = 0
        self.rolling_images_limit = rolling_images_limit

        self.value_image = None
        self.set_image()

    def set_image(self):
        self.value_image = self.dice_image.dice_images[self.number-1]

    def set_dice_value(self, value):
        self.number = value

    def rolling_animation_image(self):
        return self.dice_image.rolling_dice_images[
            self.rolling_images_counter % len(self.dice_image.rolling_dice_images)]
