import pygame
from sys import exit

from InfoProg2024.modulok.dobas_modul import DobasData
from InfoProg2024.modulok.kocka import Dice, DiceImages, DEFAULT_ROLLING_LENGTH, DEFUALT_ROLLING_INTERVAL

from enum import Enum

class State(Enum):
    MENU = 1
    GAME = 2
    HIGH_SCORES = 3

class GameStates(Enum):
    DICE_THROW = 1
    SCORING = 2
    END_GAME = 3

STATE = State.MENU

pygame.init()
clock = pygame.time.Clock()

WIDTH = 1200
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dice Roll Stimulator")

background_image = pygame.image.load('graphics/jatek_ter.png')
highlight_image = pygame.image.load('graphics/highlighter.png').convert_alpha()
rect = highlight_image.get_rect()

font = pygame.font.Font('font/SunnyspellsRegular.otf', 50)
roll_message = font.render("press SPACEBAR to start rolling", True, (255, 235, 193))



dice_rolling_images = []


dice_images = DiceImages()
# snce there are 8 rolling dice images

START_X = 70
FIRST_ROW_Y = 105
SECOND_ROW_Y = 368
DISTANCE_BETWEEN_DICES = 115

CPU_dice1 = Dice(x=START_X, y=FIRST_ROW_Y,dice_image=dice_images,rolling_images_limit=DEFAULT_ROLLING_LENGTH + DEFUALT_ROLLING_INTERVAL)
CPU_dice2 = Dice(x=START_X + DISTANCE_BETWEEN_DICES,y=FIRST_ROW_Y,dice_image=dice_images,rolling_images_limit=DEFAULT_ROLLING_LENGTH + 2*DEFUALT_ROLLING_INTERVAL)
CPU_dice3 = Dice(x=START_X + 2*DISTANCE_BETWEEN_DICES,y=FIRST_ROW_Y,dice_image=dice_images,rolling_images_limit=DEFAULT_ROLLING_LENGTH + 3*DEFUALT_ROLLING_INTERVAL)
CPU_dice4 = Dice(x=START_X + 3*DISTANCE_BETWEEN_DICES,y=FIRST_ROW_Y,dice_image=dice_images,rolling_images_limit=DEFAULT_ROLLING_LENGTH + 4*DEFUALT_ROLLING_INTERVAL)
CPU_dice5 = Dice(x=START_X + 4*DISTANCE_BETWEEN_DICES,y=FIRST_ROW_Y,dice_image=dice_images,rolling_images_limit=DEFAULT_ROLLING_LENGTH + 5*DEFUALT_ROLLING_INTERVAL)

PLAYER_dice1 = Dice(x=START_X, y=SECOND_ROW_Y,dice_image=dice_images,rolling_images_limit=DEFAULT_ROLLING_LENGTH + DEFUALT_ROLLING_INTERVAL)
PLAYER_dice2 = Dice(x=START_X + 1*DISTANCE_BETWEEN_DICES,y=SECOND_ROW_Y,dice_image=dice_images,rolling_images_limit=DEFAULT_ROLLING_LENGTH + 2*DEFUALT_ROLLING_INTERVAL)
PLAYER_dice3 = Dice(x=START_X + 2*DISTANCE_BETWEEN_DICES,y=SECOND_ROW_Y,dice_image=dice_images,rolling_images_limit=DEFAULT_ROLLING_LENGTH + 3*DEFUALT_ROLLING_INTERVAL)
PLAYER_dice4 = Dice(x=START_X + 3*DISTANCE_BETWEEN_DICES,y=SECOND_ROW_Y,dice_image=dice_images,rolling_images_limit=DEFAULT_ROLLING_LENGTH + 4*DEFUALT_ROLLING_INTERVAL)
PLAYER_dice5 = Dice(x=START_X + 4*DISTANCE_BETWEEN_DICES,y=SECOND_ROW_Y,dice_image=dice_images,rolling_images_limit=DEFAULT_ROLLING_LENGTH + 5*DEFUALT_ROLLING_INTERVAL)

CPU_dices = [CPU_dice1,CPU_dice2,CPU_dice3,CPU_dice4,CPU_dice5]
PLAYER_dices = [PLAYER_dice1,PLAYER_dice2,PLAYER_dice3,PLAYER_dice4, PLAYER_dice5 ]

dices = PLAYER_dices + CPU_dices


rolling_aud = pygame.mixer.Sound('audio/roll_aud.mp3')
rolling_stop_aud = pygame.mixer.Sound('audio/roll_stop_aud.mp3')

PLAYER_ROLL = False
#is_rolling = False
#rolling_images_counter = 0
#dice_num_image = dice_images[0]
first = True

UP_PRESSED = False
DOWN_PRESSED = False
LEFT_PRESSED = False
RIGHT_PRESSED = False

KOMBO_SZAM = 9
index = 0
HEIGHT = [100,150,200,400,500,600]
rect.x = 685
rect.y = 92
while True:

    match STATE:
        case State.MENU:
            pass

        case State.GAME:
            pass

        case State.HIGH_SCORES:
            pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not UP_PRESSED:
                                                           
                UP_PRESSED = True
                print("UP PRESSED")

                if index > 0:
                    index -= 1
                    rect.y -= 52

            if event.key == pygame.K_DOWN and not DOWN_PRESSED:
                DOWN_PRESSED = True
                print("DOWN PRESSED")
                print(index)
                if index < KOMBO_SZAM - 1:
                    index += 1
                    rect.y += 52

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and UP_PRESSED:
                UP_PRESSED = False
                print("UP UNPRESSED")

            if event.key == pygame.K_DOWN and DOWN_PRESSED:
                DOWN_PRESSED = False
                print("DOWN UNPRESSED")

    screen.blit(background_image, (0, 0))
    screen.blit(roll_message, (50, 300))

    screen.blit(highlight_image,rect)

    key = pygame.key.get_pressed()





    if key[pygame.K_SPACE] and PLAYER_ROLL is False:

        CPU_dobas_data = DobasData()
        PLAYER_dobas_data= DobasData()

        print("CPU",CPU_dobas_data)
        print("PLAYER",PLAYER_dobas_data)

        rolling_aud.play()


        PLAYER_ROLL = True

        for d in dices:
            d.is_rolling = True
            if(d in PLAYER_dices):
                d.set_dice_value(PLAYER_dobas_data.get_next())
            else:
                d.set_dice_value(CPU_dobas_data.get_next())
            d.set_image()

            screen.blit(d.rolling_animation_image(), (d.x, d.y))
            #screen.blit(dice_rolling_images[rolling_images_counter], (250, 150))
            d.rolling_images_counter += 1
            #rolling_images_counter += 1
        first = True

        # start rolling and calculate dice num
    else:
        if PLAYER_ROLL:
            # showing rolling animation images
            for d in dices:
                if not d.is_rolling:
                    screen.blit(d.value_image, (d.x, d.y))
                    continue

                screen.blit(d.rolling_animation_image(),(d.x, d.y))
            #screen.blit(dice_rolling_images[rolling_images_counter], (250, 150))
                d.rolling_images_counter += 1
                if d.rolling_images_counter >= d.rolling_images_limit:
                    d.is_rolling = False
                    d.rolling_images_counter = 0
                    rolling_stop_aud.play()
                    #screen.blit(d.value_image, (d.x, d.y))


            if not any(x.is_rolling == True for x in dices):
                print("here")
                PLAYER_ROLL = False
        else:
            for d in dices:
                screen.blit(d.value_image, (d.x, d.y))
                #screen.blit(dice_num_image, (250, 150))
            if first:
                rolling_stop_aud.play()
                first = False
            # show the dice which contains a number

    pygame.display.update()
    clock.tick(13)