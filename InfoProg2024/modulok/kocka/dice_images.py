import pygame


class DiceImages:
    def __init__(self):
        self.dice_images = self.load_dice_images()
        self.rolling_dice_images = self.load_rolling_dice_images()

    @staticmethod
    def load_dice_images():
        images = []
        for num in range(1, 7):
            dice_image = pygame.image.load('graphics/dice2/' + str(num) + '.png')
            images.append(dice_image)

        return images

    @staticmethod
    def load_rolling_dice_images():
        rolling_dice_image = []
        for num in range(1, 9):
            dice_rolling_image = pygame.image.load('graphics/animation2/roll' + str(num) + '.png')
            rolling_dice_image.append(dice_rolling_image)

        return rolling_dice_image
