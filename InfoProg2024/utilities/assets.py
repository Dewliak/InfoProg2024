import pygame


class FontColors:
    """
    A betűtípusok színeit foglalja egybe
    """
    cream = (255, 235, 193)
    yellow = (255, 235, 33)
    dark_cream = (105, 98, 85)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)


class TextBox:
    """
    A szöveg köré egy téglalapot alakít ki
    """
    def __init__(self, screen, text: str, pos_x: int, pos_y: int, font, text_box_image: pygame.image):
        """

        :param screen:
        :param text:
        :param pos_x:
        :param pos_y:
        :param font:
        :param text_box_image:
        """
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


# Képek, hátterek,...
icon = pygame.image.load("graphics/icon.ico")
background_image = pygame.image.load('graphics/jatek_ter.png')
turn_pointer = pygame.image.load('graphics/turn_pointer.png')
main_menu_background_image = pygame.image.load('graphics/main_menu.png')
menu_pointer_image = pygame.image.load('graphics/pointer.png')
high_scores_image = pygame.image.load('graphics/highscore_image.png')
settings_image = pygame.image.load('graphics/settings_image.png')
settings_check_box = pygame.image.load('graphics/settings_check_box.png')
settings_check = pygame.image.load('graphics/check.png')

hello_screen_image = pygame.image.load('graphics/hello_screen.png')

highlight_image = pygame.image.load('graphics/highlighter.png').convert_alpha()
highlight_image_rectangle = highlight_image.get_rect()
highlight_image_rectangle.x = 684
highlight_image_rectangle.y = 92
HIGLIGHT_DELTA = 46 # Mekkorát ugorjon a téglalap

# A vizuális billentyűk képei
keyboard_up_1 = pygame.image.load('graphics/keyboard/UP_1.png')
keyboard_up_2 = pygame.image.load('graphics/keyboard/UP_2.png')
keyboard_down_1 = pygame.image.load('graphics/keyboard/DOWN_1.png')
keyboard_down_2 = pygame.image.load('graphics/keyboard/DOWN_2.png')
keyboard_space_1 = pygame.image.load('graphics/keyboard/SPACE_1.png')
keyboard_space_2 = pygame.image.load('graphics/keyboard/SPACE_2.png')
keyboard_enter_1 = pygame.image.load('graphics/keyboard/ENTER_1.png')
keyboard_enter_2 = pygame.image.load('graphics/keyboard/ENTER_2.png')
keyboard_s_1 = pygame.image.load('graphics/keyboard/s_1.png')
keyboard_s_2 = pygame.image.load('graphics/keyboard/s_2.png')

text_box = pygame.image.load('graphics/text_box.png')
text_box_2 = pygame.image.load('graphics/text_box_2.png')

score_board_box_1 = pygame.image.load('graphics/score_board_1.png')
score_board_box_2 = pygame.image.load('graphics/score_board_2.png')
endgame_bg = pygame.image.load('graphics/endgame_bg.png')



save_button = pygame.image.load('graphics/save_button/save_button.png')
save_button_rect = save_button.get_rect()
un_pressed_save_button = pygame.image.load('graphics/save_button/un_pressed.png')
un_pressed_save_button_rect = un_pressed_save_button.get_rect()
# Betűtípus
font = pygame.font.Font('font/SunnyspellsRegular.otf', 50)
highscore_font = pygame.font.Font('font/SunnyspellsRegular.otf', 30)
highscore_menu_font = pygame.font.Font('font/SunnyspellsRegular.otf', 45)
tooltip_font = pygame.font.Font('font/prstartk.ttf', 13)
endgame_font = pygame.font.Font('font/SunnyspellsRegular.otf',105)
restart_font = pygame.font.Font('font/prstartk.ttf',18)

# Hangok
rolling_aud = pygame.mixer.Sound('audio/roll_aud.mp3')
rolling_stop_aud = pygame.mixer.Sound('audio/roll_stop_aud.mp3')

#Menü szövegek
continue_game = font.render("Folytatás", True, FontColors.cream)
no_continue_game = font.render("Folytatás", True, FontColors.dark_cream)
new_game = font.render("Új játék", True, FontColors.cream)
high_scores = font.render("Rangsor", True, FontColors.cream)
settings = font.render("Beállítások", True, FontColors.cream)

