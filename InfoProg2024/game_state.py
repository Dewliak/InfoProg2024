import pygame
from sys import exit

from InfoProg2024.modulok.dobas_modul import DobasData
from InfoProg2024.modulok.kocka import Dice, DiceImages, DEFAULT_ROLLING_LENGTH, DEFUALT_ROLLING_INTERVAL

from enum import Enum

class GameStates(Enum):
    DICE_THROW = 1
    SCORING = 2
    END_GAME = 3





# snce there are 8 rolling dice images

def game_state(screen):
    background_image = pygame.image.load('graphics/green_matt.jpg')
    highlight_image = pygame.image.load('graphics/highlighter.png').convert_alpha()
    rect = highlight_image.get_rect()

    font = pygame.font.Font('font/SunnyspellsRegular.otf', 50)
    roll_message = font.render("press SPACEBAR to start rolling", True, (255, 235, 193))

    dice_images = DiceImages()

    CPU_dice1 = Dice(x=30, y=30, dice_image=dice_images,
                     rolling_images_limit=DEFAULT_ROLLING_LENGTH + DEFUALT_ROLLING_INTERVAL)
    CPU_dice2 = Dice(x=160, y=30, dice_image=dice_images,
                     rolling_images_limit=DEFAULT_ROLLING_LENGTH + 2 * DEFUALT_ROLLING_INTERVAL)
    CPU_dice3 = Dice(x=300, y=30, dice_image=dice_images,
                     rolling_images_limit=DEFAULT_ROLLING_LENGTH + 3 * DEFUALT_ROLLING_INTERVAL)
    CPU_dice4 = Dice(x=440, y=30, dice_image=dice_images,
                     rolling_images_limit=DEFAULT_ROLLING_LENGTH + 4 * DEFUALT_ROLLING_INTERVAL)
    CPU_dice5 = Dice(x=580, y=30, dice_image=dice_images,
                     rolling_images_limit=DEFAULT_ROLLING_LENGTH + 5 * DEFUALT_ROLLING_INTERVAL)

    PLAYER_dice1 = Dice(x=30, y=250, dice_image=dice_images,
                        rolling_images_limit=DEFAULT_ROLLING_LENGTH + DEFUALT_ROLLING_INTERVAL)
    PLAYER_dice2 = Dice(x=160, y=250, dice_image=dice_images,
                        rolling_images_limit=DEFAULT_ROLLING_LENGTH + 2 * DEFUALT_ROLLING_INTERVAL)
    PLAYER_dice3 = Dice(x=300, y=250, dice_image=dice_images,
                        rolling_images_limit=DEFAULT_ROLLING_LENGTH + 3 * DEFUALT_ROLLING_INTERVAL)
    PLAYER_dice4 = Dice(x=440, y=250, dice_image=dice_images,
                        rolling_images_limit=DEFAULT_ROLLING_LENGTH + 4 * DEFUALT_ROLLING_INTERVAL)
    PLAYER_dice5 = Dice(x=580, y=250, dice_image=dice_images,
                        rolling_images_limit=DEFAULT_ROLLING_LENGTH + 5 * DEFUALT_ROLLING_INTERVAL)

    dices = [CPU_dice1, CPU_dice2, CPU_dice3, CPU_dice4, CPU_dice5]
    PLAYER_dices = [PLAYER_dice1, PLAYER_dice2, PLAYER_dice3, PLAYER_dice4, PLAYER_dice5]

    rect = pygame.Rect(0, 0, 300, 60)

    rect.x = 700
    rolling_aud = pygame.mixer.Sound('audio/roll_aud.mp3')
    rolling_stop_aud = pygame.mixer.Sound('audio/roll_stop_aud.mp3')

    PLAYER_ROLL = False
    # is_rolling = False
    # rolling_images_counter = 0
    # dice_num_image = dice_images[0]
    first = True

    UP_PRESSED = False
    DOWN_PRESSED = False
    LEFT_PRESSED = False
    RIGHT_PRESSED = False

    KOMBO_SZAM = 9
    index = 0
    HEIGHT = [100, 150, 200, 400, 500, 600]

    screen.blit(background_image, (0, 0))
    screen.blit(roll_message, (50, 300))

    pygame.draw.rect(screen, (255, 0, 255), rect)
    screen.blit(highlight_image, rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not UP_PRESSED:
                UP_PRESSED = True
                print("UP PRESSED")
                # if index < 0:
                index += 1
                rect.y += 40
                # rect.y = HEIGHT[index]

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and UP_PRESSED:
                UP_PRESSED = False
                print("UP UNPRESSED")

    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE] and PLAYER_ROLL is False:

        dobas_data = DobasData()
        print(dobas_data)
        rolling_aud.play()

        rect.move(200, 200)
        rect.x += 10

        PLAYER_ROLL = True

        for index, d in enumerate(dices):
            d.is_rolling = True
            d.set_dice_value(dobas_data[index])
            d.set_image()

            screen.blit(d.rolling_animation_image(), (d.x, d.y))
            # screen.blit(dice_rolling_images[rolling_images_counter], (250, 150))
            d.rolling_images_counter += 1
            # rolling_images_counter += 1
        first = True

        # start rolling and calculate dice num
    else:
        if PLAYER_ROLL:
            # showing rolling animation images
            for d in dices:
                if not d.is_rolling:
                    screen.blit(d.value_image, (d.x, d.y))
                    continue

                screen.blit(d.rolling_animation_image(), (d.x, d.y))
                # screen.blit(dice_rolling_images[rolling_images_counter], (250, 150))
                d.rolling_images_counter += 1
                if d.rolling_images_counter >= d.rolling_images_limit:
                    d.is_rolling = False
                    d.rolling_images_counter = 0
                    # screen.blit(d.value_image, (d.x, d.y))

            if not any(x.is_rolling == True for x in dices):
                print("here")
                PLAYER_ROLL = False
        else:
            for d in dices:
                screen.blit(d.value_image, (d.x, d.y))
                # screen.blit(dice_num_image, (250, 150))
            if first:
                rolling_stop_aud.play()
                first = False

