import pygame
from typing import Tuple
class FontColors:
    cream = (255, 235, 193)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

class TextBox:
    def __init__(self, screen, text: str, pos_x: int, pos_y: int, font,text_box_image: pygame.image):
        self.screen = screen
        self.text = text

        self.text_box_image = text_box_image
        self.rect = self.text_box_image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.rendered_text = font.render(text, True, (255, 255, 255))
        self.rendered_text_rect = self.rendered_text.get_rect()
        self.rendered_text_rect.center = (pos_x, pos_y)


        self.pos_x = pos_x
        self.pos_y = pos_y

    def render(self):
        self.screen.blit(self.text_box_image, self.rect)
        self.screen.blit(self.rendered_text, self.rendered_text_rect)


background_image = pygame.image.load('graphics/jatek_ter.png')
main_menu_background_image = pygame.image.load('graphics/main_menu.png')
menu_pointer_image = pygame.image.load('graphics/pointer.png')
high_scores_image = pygame.image.load('graphics/highscore_image.png')
settings_image = pygame.image.load('graphics/settings_image.png')
highlight_image = pygame.image.load('graphics/highlighter.png').convert_alpha()
highlight_image_rectangle = highlight_image.get_rect()
highlight_image_rectangle.x = 684
highlight_image_rectangle.y = 92
HIGLIGHT_DELTA = 46

settings_check_box = pygame.image.load('graphics/settings_check_box.png')
settings_check = pygame.image.load('graphics/check.png')

turn_pointer = pygame.image.load('graphics/turn_pointer.png')


font = pygame.font.Font('font/SunnyspellsRegular.otf', 50)
highscore_font = pygame.font.Font('font/SunnyspellsRegular.otf', 30)
highscore_menu_font = pygame.font.Font('font/SunnyspellsRegular.otf', 45)
tooltip_font = pygame.font.Font('font/prstartk.ttf', 13)
endgame_font = pygame.font.Font('font/SunnyspellsRegular.otf',105)
restart_font = pygame.font.Font('font/prstartk.ttf',18)


rolling_aud = pygame.mixer.Sound('audio/roll_aud.mp3')
rolling_stop_aud = pygame.mixer.Sound('audio/roll_stop_aud.mp3')

#Menu messages
continue_game = font.render("Continue", True, FontColors.cream)
new_game = font.render("New game", True, FontColors.cream)
high_scores = font.render("Highscores", True, FontColors.cream)
settings = font.render("Settings", True, FontColors.cream)

keyboard_up_1 = pygame.image.load('graphics/keyboard/UP_1.png')
keyboard_up_2 = pygame.image.load('graphics/keyboard/UP_2.png')
keyboard_down_1 = pygame.image.load('graphics/keyboard/DOWN_1.png')
keyboard_down_2 = pygame.image.load('graphics/keyboard/DOWN_2.png')
keyboard_space_1 = pygame.image.load('graphics/keyboard/SPACE_1.png')
keyboard_space_2 = pygame.image.load('graphics/keyboard/SPACE_2.png')
keyboard_enter_1 = pygame.image.load('graphics/keyboard/ENTER_1.png')
keyboard_enter_2 = pygame.image.load('graphics/keyboard/ENTER_2.png')

text_box = pygame.image.load('graphics/text_box.png')

score_board_box_1 = pygame.image.load('graphics/score_board_1.png')
score_board_box_2 = pygame.image.load('graphics/score_board_2.png')
endgame_bg = pygame.image.load('graphics/endgame_bg.png')

class GameText:

    end_game_text_cpu_win = "The winner is: the CPU"
    end_game_text_player_win = "The winner is: the {name}"