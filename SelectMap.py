import pygame
from pygame.locals import *
from constantes import*

class SelectMap:
    def __init__(self):
        self.images_background = pygame.image.load("source/images/select_editor_background.png")
        self.list_map = []

    def display_select_map(self,surface):
        surface.blit(self.images_background, (0, 0))


    def select_map(self, surface):
        i = 1
        for line_box in range(5):
            for item_box in range(1):
                x = BOARD_TOPLEFT[0]*2 + item_box * (CELL_SIZE[0] + CELL_SPACING[0])
                y = BOARD_TOPLEFT[1] + line_box * (CELL_SIZE[1] + CELL_SPACING[1])
                #pygame.draw.rect(surface, COLOR_LIST[9], (x, y, CELL_SIZE[0]*5 + 20 , CELL_SIZE[1]//1.7), 2)
                #font = pygame.font.Font(None, 24)
                font = pygame.font.Font("source/font/Liebing.ttf",48)
                custom_map = font.render('Custom Map {}'.format(i), 1, (255, 255, 255))  # CHOISIR NOMBRE DE JOUEUR
                surface.blit(custom_map, (x, y))
                i+=1
