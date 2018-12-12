import pygame
from constantes import*

class Menu:
    """Create Menu object"""
    def __init__(self):
        
        self.image_background = pygame.image.load("source/images/menu_background.png").convert()
        self.arrow_underline = pygame.image.load("source/images/arrow_underline.png")
        self.arrow_underline_X = 66
        self.arrow_underline_Y = 130
        self.button_play_X = 528
        self.button_play_Y = 268
        self.button_play_size = (225, 300)

        self.button_editor_X = 1047
        self.button_editor_Y =0
        self.button_editor_size = (193,280)

        self.list_map = ["Classic", "Imhotep", "Dynasty", "Custom"]
        self.index_map = 0

    def display_menu(self,surface):
        surface.blit(self.image_background, (0, 0))
        surface.blit(self.arrow_underline, (self.arrow_underline_X, self.arrow_underline_Y))
        pygame.display.update()


    def change_map(self, position):
        if 95 <= position[0] <= 170 and 105 <= position[1] <= 135:
            self.index_map = 0
            self.arrow_underline_Y = 130
            return True
        elif 95 <= position[0] <= 175 and 140 <= position[1] <= 175:
            self.index_map = 1
            self.arrow_underline_Y = 170
            return True
        elif 95 <= position[0] <= 175 and 180 <= position[1] <= 210:
            self.index_map = 2
            self.arrow_underline_Y = 205
            return True
        return False

    def start_game(self, position):
        #print(position)
        if self.button_play_X <= position[0] <= self.button_play_X + self.button_play_size[0] and self.button_play_Y <= position[1] <= self.button_play_Y + self.button_play_size[1]:
            return True
        return False

    def start_editor(self, position):
        if self.button_editor_X <= position[0] <= self.button_editor_X + self.button_editor_size[0] and self.button_editor_Y <= position[1] <= self.button_editor_Y + self.button_editor_size[1]:
            return True
        return False

    def hand_cursor(self, position, surface):
        if self.button_play_X <= position[0] <= self.button_play_X + self.button_play_size[0] and self.button_play_Y <= position[1] <= self.button_play_Y + self.button_play_size[1]:
            pointerImg = pygame.image.load('source/images/sword_icon.png')
            pointerImg_rect = pointerImg.get_rect()
            pointerImg_rect.center = pygame.mouse.get_pos()
            surface.blit(pointerImg, pointerImg_rect)
