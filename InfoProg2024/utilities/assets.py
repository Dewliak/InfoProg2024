import pygame

background_image = pygame.image.load('graphics/jatek_ter.png')
highlight_image = pygame.image.load('graphics/highlighter.png').convert_alpha()
highlight_image_rectangle = highlight_image.get_rect()
highlight_image_rectangle.x = 684
highlight_image_rectangle.y = 92
HIGLIGHT_DELTA = 46

font = pygame.font.Font('font/SunnyspellsRegular.otf', 50)
roll_message = font.render("press SPACEBAR to start rolling", True, (255, 235, 193))

rolling_aud = pygame.mixer.Sound('audio/roll_aud.mp3')
rolling_stop_aud = pygame.mixer.Sound('audio/roll_stop_aud.mp3')