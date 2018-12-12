import pygame
from shutil import move
import os
from Pawn import*
from constantes import*
import pickle



class Editor:


    def __init__(self):
        pawn = Pawn('pharaoh', 'player_one', 'south')
        self.image_background = pygame.image.load("source/images/editor_background.png").convert()
        self.list_pawn = []
        self.list_starter_pawn = [['pharaoh', 'anubis', 'scarab', 'pyramid'], [pawn, pawn, pawn, pawn]]
        self.list_starter_box = []
        self.list_box_editor = []
        self.button_direction_size = (105, 30)
        self.button_player_size = (78, 80)
        self.button_map_size = (186, 75)
        self.list_custom_map = []
        self.num_custom_map = []

    def starter_pawn(self,surface):
        """Generate starters panws into banener"""
        line_box = 0
        item_box = 0
        for em in range(4):
            x = BOARD_STARTER_TOPLEFT_EDITOR[0] + item_box * (CELL_SIZE[0] + CELL_SPACING_EDITOR[0])
            y = BOARD_STARTER_TOPLEFT_EDITOR[1] + line_box * (CELL_SIZE[1] + CELL_SPACING_EDITOR[1])
            #print(self.list_box[em]._get_pos_X)

            box = Box('player_one', False)
            box._set_pos_X(x)
            box._set_pos_Y(y)
            box._set_box_color(int(9))
            self.list_starter_box.append(box)


            pawn = Pawn(self.list_starter_pawn[0][line_box], 'player_one', 'south')
            pawn._set_pos_X(x)
            pawn._set_pos_Y(y)
            self.list_starter_pawn[1][line_box] = pawn
            item_box+=1
            if item_box % 1 == 0:
                line_box+=1
                item_box=0

    def generate_map(self,surface,color_list):
        """Generate an empty map with only Corssbows"""
        for line in range(8):
            for item in range(10):
                x = BOARD_TOPLEFT_EDITOR[0] + item * (CELL_SIZE[0] + CELL_SPACING[0])
                y = BOARD_TOPLEFT_EDITOR[1] + line * (CELL_SIZE[1] + CELL_SPACING[1])
                box = Box('neutral', True)
                box._set_pos_X(x)
                box._set_pos_Y(y)
                box._set_box_color(int(9))
                self.list_box_editor.append(box)
        self.list_box_editor[0].box_is_empty = False
        self.list_box_editor[79].box_is_empty = False


        pawn_one = Sphinx('sphinx', 'player_one', 'south')
        pawn_one._set_pos_X(BOARD_TOPLEFT_EDITOR[0])
        pawn_one._set_pos_Y(BOARD_TOPLEFT_EDITOR[1])
        self.list_pawn.append(pawn_one)

        pawn_two = Sphinx('sphinx', 'player_two', 'north')
        pawn_two._set_pos_X(self.list_box_editor[79]._get_pos_X())
        pawn_two._set_pos_Y(self.list_box_editor[79]._get_pos_Y())
        self.list_pawn.append(pawn_two)

    def draw_map(self, surface):
        surface.blit(self.image_background, (0, 0))
        line_box = 0
        item_box = 0

        line_starter_box = 0
        item_starter_box = 0

        #Image for special boxes
        for em in range(len(self.list_box_editor)):
            x = self.list_box_editor[em]._get_pos_X()
            y = self.list_box_editor[em]._get_pos_Y()
            if self.list_box_editor[em].owner_box == 'player_one_fix' or self.list_box_editor[em].owner_box == 'player_two_fix':
                appearance_box = pygame.image.load(self.list_box_editor[em].image_box)
                surface.blit(appearance_box, (x, y))

        #grid on board editor
        for em in range(len(self.list_box_editor)):
            x = BOARD_TOPLEFT_EDITOR[0] + item_box * (CELL_SIZE[0] + CELL_SPACING[0])
            y = BOARD_TOPLEFT_EDITOR[1] + line_box * (CELL_SIZE[1] + CELL_SPACING[1])
            #print(self.list_box[em]._get_pos_X)
            pygame.draw.rect(surface, COLOR_LIST[self.list_box_editor[em]._get_box_color()], (x, y, CELL_SIZE[0], CELL_SIZE[1]), 5)
            item_box+=1
            if item_box % 10 == 0:
                line_box+=1
                item_box=0

        #box for starters pawns
        for em in range(len(self.list_starter_box)):
            x = BOARD_STARTER_TOPLEFT_EDITOR[0] + item_starter_box * (CELL_SIZE[0] + CELL_SPACING_EDITOR[0])
            y = BOARD_STARTER_TOPLEFT_EDITOR[1]+ line_starter_box * (CELL_SIZE[1] + CELL_SPACING_EDITOR[1])
            #print(self.list_box[em]._get_pos_X)
            pygame.draw.rect(surface, COLOR_LIST[self.list_starter_box[em]._get_box_color()], (x, y, CELL_SIZE[0], CELL_SIZE[1]), 5)
            item_starter_box+=1
            if item_starter_box % 1 == 0:
                line_starter_box+=1
                item_starter_box=0
        #images for starters pawns
        for em in range(len(self.list_starter_pawn[1])):
            x = self.list_starter_pawn[1][em]._get_pos_X()
            y = self.list_starter_pawn[1][em]._get_pos_Y()
            appearance_pawn = pygame.image.load(self.list_starter_pawn[1][em].image_pawn)
            surface.blit(appearance_pawn, (x-20, y-114))
        #image for pawns
        for line_box in range(8):
            for item_box in range(10):
                x = BOARD_TOPLEFT_EDITOR[0] + item_box * (CELL_SIZE[0] + CELL_SPACING[0])
                y = BOARD_TOPLEFT_EDITOR[1] + line_box * (CELL_SIZE[1] + CELL_SPACING[1])
                for em in range(len(self.list_pawn)):
                    pawn_X = self.list_pawn[em]._get_pos_X()
                    pawn_Y = self.list_pawn[em]._get_pos_Y()
                    if pawn_X == x and pawn_Y == y:
                        appearance_pawn = pygame.image.load(self.list_pawn[em].image_pawn)
                        surface.blit(appearance_pawn, (x-20, y-114))



    def select_pawn_editor(self, surface):
        """Select a pawn on editor board"""
        position = pygame.mouse.get_pos()
        for line_box in range(8):
            for item_box in range(10):
                x = BOARD_STARTER_TOPLEFT_EDITOR[0] + item_box * (CELL_SIZE[0] + CELL_SPACING_EDITOR[0])
                y = BOARD_STARTER_TOPLEFT_EDITOR[1]+ line_box * (CELL_SIZE[1] + CELL_SPACING_EDITOR[1])
                if x <= position[0] <= x + CELL_SIZE[0] and y <= position[1] <= y + CELL_SIZE[1]:
                    for el in range(len(self.list_starter_box)): #iterate on whole box
                        box_X = self.list_starter_box[el]._get_pos_X()
                        box_Y = self.list_starter_box[el]._get_pos_Y()
                        if x == box_X and y == box_Y: #For box at coord = click
                            for em in range(5):
                                #Get coordinate Pawn in list of Pawn
                                pawn_X = self.list_starter_pawn[1][em]._get_pos_X()
                                pawn_Y = self.list_starter_pawn[1][em]._get_pos_Y()
                                if box_X == pawn_X and box_Y == pawn_Y:
                                    pygame.draw.rect(surface, COLOR_LIST[2], (x, y, CELL_SIZE[0], CELL_SIZE[1]), 5)
                                    self.list_starter_pawn[1][em].pawn_is_select = True
                                    return (True, x, y, el, em) #Can select a pawn, at x y coordinate
                                    # and his place in list is "em"):

    def edit_attributs_pawn(self, index_box):
        """get pawn's index on editor board"""
        box_X = self.list_box_editor[index_box]._get_pos_X()
        box_Y = self.list_box_editor[index_box]._get_pos_Y()
        for em in range(len(self.list_pawn)):
            #Get coordinate Pawn in list of Pawn
            pawn_X = self.list_pawn[em]._get_pos_X()
            pawn_Y = self.list_pawn[em]._get_pos_Y()
            if box_X == pawn_X and box_Y == pawn_Y:
                return em #Can select a pawn, at x y coordinate
                # and his place in list is "em"):


    def settings_pawn(self, position, index_pawn, index_box):
        """ Set Attributs of each pawn """
        x =  self.list_box_editor[index_box]._get_pos_X()
        y =  self.list_box_editor[index_box]._get_pos_Y()

        if self.list_box_editor[index_box].box_is_empty == False:

            if 485 <= position[0] <= 485 + self.button_direction_size[0] and 620 <= position[1] <= 620 + self.button_direction_size[1]:
                self.list_pawn[index_pawn].direction_pawn = 'north'

            elif 485 <= position[0] <= 485 + self.button_direction_size[0] and 660 <= position[1] <= 660 + self.button_direction_size[1]:
                self.list_pawn[index_pawn].direction_pawn = 'south'

            elif 826 <= position[0] <= 826 + self.button_direction_size[0] and 620 <= position[1] <= 620 + self.button_direction_size[1]:
                self.list_pawn[index_pawn].direction_pawn = 'east'

            elif 826 <= position[0] <= 826 + self.button_direction_size[0] and 620 <= position[1] <= 660 + self.button_direction_size[1]:
                self.list_pawn[index_pawn].direction_pawn = 'west'

            elif 308 <= position[0] <= 308 + self.button_player_size[0] and 625 <= position[1] <= 625 + self.button_player_size[1]: #lion
                self.list_pawn[index_pawn].owner_pawn = 'player_one'

            elif 1026 <= position[0] <= 1026 + self.button_player_size[0] and 618 <= position[1] <= 618 + self.button_player_size[1]: #aigle
                self.list_pawn[index_pawn].owner_pawn = 'player_two'
                if self.list_box_editor[index_box].owner_box != 'player_two_fix':
                    self.list_box_editor[index_box].owner_box = 'player_two'

            self.list_pawn[index_pawn].image_pawn = "source/images/{}_{}_{}.png".format(self.list_pawn[index_pawn].name_pawn,
            self.list_pawn[index_pawn].owner_pawn, self.list_pawn[index_pawn].direction_pawn)

        else:
            if 308 <= position[0] <= 308 + self.button_player_size[0] and 625 <= position[1] <= 625 + self.button_player_size[1]: #lion
                self.list_box_editor[index_box].owner_box = 'player_one_fix'
                self.list_box_editor[index_box].image_box = 'source/images/player_one_fix.png'

            elif 1026 <= position[0] <= 1026 + self.button_player_size[0] and 618 <= position[1] <= 618 + self.button_player_size[1]: #aigle
                self.list_box_editor[index_box].owner_box = 'player_two_fix'
                self.list_box_editor[index_box].image_box = 'source/images/player_two_fix.png'


        pygame.display.update()



    def generate_file_custom_map(self):

        """generate multiple files for each map"""

        with open('source/map/number_custom_map', 'r') as file:
            self.num_custom_map = file.read().splitlines()

        with open('source/map/custom_pawn_{}'.format(len(self.num_custom_map)), 'wb') as fichier:
            my_pickler = pickle.Pickler(fichier)
            for line_box in range(8):
                for item_box in range(10):
                    x = BOARD_TOPLEFT_EDITOR[0] + item_box * (CELL_SIZE[0] + CELL_SPACING[0])
                    y = BOARD_TOPLEFT_EDITOR[1] + line_box * (CELL_SIZE[1] + CELL_SPACING[1])
                    for em in range(len(self.list_pawn)):
                        pawn_X = self.list_pawn[em]._get_pos_X()
                        pawn_Y = self.list_pawn[em]._get_pos_Y()
                        if pawn_X == x and pawn_Y == y:
                            my_pickler.dump((self.list_pawn[em]))

        with open('source/map/custom_box_{}'.format(len(self.num_custom_map)), 'wb') as file:
            my_pickler = pickle.Pickler(file)
            for line_box in range(8):
                for item_box in range(10):
                    x = BOARD_TOPLEFT_EDITOR[0] + item_box * (CELL_SIZE[0] + CELL_SPACING[0])
                    y = BOARD_TOPLEFT_EDITOR[1] + line_box * (CELL_SIZE[1] + CELL_SPACING[1])
                    for el in range(len(self.list_box_editor)):
                        box_X = self.list_box_editor[el]._get_pos_X()
                        box_Y = self.list_box_editor[el]._get_pos_Y()
                        if box_X == x and box_Y == y:
                            my_pickler.dump((self.list_box_editor[el]))

        with open('source/map/number_custom_map', 'a') as file:
            file.write("Custom_map_{} {}\n".format(len(self.num_custom_map), len(self.list_pawn)))
            file.seek(0)

        self.nbr_pawn = self.list_custom_map

    def search_number_custom_map(self):
        with open('source/map/number_custom_map', 'r') as file:
            self.list_custom_map = file.read().splitlines()
            for i in range (len(self.list_custom_map)):
                self.list_custom_map[i] = self.list_custom_map[i].split(" ")



    def max_map(self):
        """ Check if they are more than 5 maps"""

        if len(self.num_custom_map) >= 5:
            with open('source/map/number_custom_map', 'w') as file:
                #delete first files
                os.remove('source/map/custom_pawn_0')
                os.remove('source/map/custom_box_0')
                #the second file rename into first one etc
                for j in range(len(self.num_custom_map)):
                    move('source/map/custom_pawn_{}'.format(j+1), 'source/map/custom_pawn_{}'.format(j))
                    move('source/map/custom_box_{}'.format(j+1), 'source/map/custom_box_{}'.format(j))
                    file.write("Custom_map_{} {}\n".format(0, self.list_custom_map[0][1]))
                    file.seek(0)
            with open('source/map/number_custom_map', 'a') as file:
                for j in range(1,len(self.num_custom_map)):
                    file.write("Custom_map_{} {}\n".format(j, self.list_custom_map[j+1][1]))
                    file.seek(0)

            del self.list_custom_map[0]

            with open('source/map/number_custom_map', 'r') as file:
                self.num_custom_map = file.read().splitlines()
            with open('source/map/number_custom_map', 'r') as file:
                self.list_custom_map = file.read().splitlines()
                for i in range (len(self.list_custom_map)):
                    self.list_custom_map[i] = self.list_custom_map[i].split(" ")
            self.num_custom_map = 4
            return True

    def start_custom_game(self, map, boolean_Max):
        """ Save to list object saved in files """
        list_custom_pawn = []
        list_custom_box = []

        with open('source/map/custom_pawn_{}'.format(map), 'rb') as fichier:
            my_depickler = pickle.Unpickler(fichier)
            if boolean_Max == True:
                j = 1
            else:
                j = 0
            for i in range(int(self.list_custom_map[map][1])+j):
                pawn = my_depickler.load()
                list_custom_pawn.append(pawn)
        with open('source/map/custom_box_{}'.format(map), 'rb') as fichier:
            my_depickler = pickle.Unpickler(fichier)
            for i in range(len(self.list_box_editor)):
                pawn = my_depickler.load()
                list_custom_box.append(pawn)
        return list_custom_pawn, list_custom_box
