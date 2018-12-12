import pygame

from Pawn import*
from Box import*
from algorithms import *
from constantes import*


class Map:
    """Generate map"""
    def __init__(self,name_map):
        """initialize attributs
            - self.list_name = [] : stock name's pawn from a map's file
            - self.list_box_owner = [] : stock box's pawn from a map's file
            - self.list_direction = [] : stock direction's pawn from a map's file
        """
        self.name_map = name_map
        self.rows = 8
        self.columns = 10
        self.list_name = []
        self.list_pawn = []
        self.list_box_owner = []
        self.list_box = []
        self.list_direction = []
        self.end_game = False

    def generate_list_name(self):
        """Generate a name's pawn's list"""
        with open('source/map/map_{}'.format(self.name_map), 'r') as my_file_name:
            self.list_name = my_file_name.read().splitlines()
            for i in range (8):
                self.list_name[i] = self.list_name[i].split(" ")
            return self.list_name

    def generate_list_owner(self):
        """Generate a name's box's list"""
        with open('source/map/box_{}'.format(self.name_map), 'r') as my_file_name:
            self.list_box_owner = my_file_name.read().splitlines()
            for i in range (8):
                self.list_box_owner[i] = self.list_box_owner[i].split(" ")
            return self.list_box_owner


    def generate_list_direction(self):
        """Generate a 's pawns's list"""
        with open('source/map/direction_{}'.format(self.name_map), 'r') as my_file_direction:
            self.list_direction = my_file_direction.read().splitlines()
            for i in range (8):
                self.list_direction[i] = self.list_direction[i].split(" ")

            return self.list_direction

    def generate_map(self,surface,color_liste, list_box):
        """Generate Map, create Pawns objects and Box objects"""
        #iterate our board
        for line in range(self.rows):
            for item in range(self.columns):
                x = BOARD_TOPLEFT[0] + item * (CELL_SIZE[0] + CELL_SPACING[0])
                y = BOARD_TOPLEFT[1] + line * (CELL_SIZE[1] + CELL_SPACING[1])
                if self.list_name[line][item] != 'nothing': # if name is not 'nothing'
                    if self.list_box_owner[line][item] == "player_one" or self.list_box_owner[line][item] == "player_one_fix":
                        owner_pawn = "player_one" #whatever box is fix or not, the owner would be same
                    else : owner_pawn = "player_two"

                    #use specific class to create pawns
                    if self.list_name[line][item] == "pharaoh":
                        pawn = Pharaoh(self.list_name[line][item], owner_pawn, self.list_direction[line][item])
                    elif self.list_name[line][item] == "anubis":
                        pawn = Anubis(self.list_name[line][item], owner_pawn, self.list_direction[line][item])
                    elif self.list_name[line][item] == "scarab":
                        pawn = Scarab(self.list_name[line][item], owner_pawn, self.list_direction[line][item])
                    elif self.list_name[line][item] == "pyramid":
                        pawn = Pyramid(self.list_name[line][item], owner_pawn, self.list_direction[line][item])
                    elif self.list_name[line][item] == "sphinx":
                        pawn = Sphinx(self.list_name[line][item], owner_pawn, self.list_direction[line][item])
                    else : print("ERROR Pawn does not exit !")
                    #set position of pawns
                    pawn._set_pos_X(x)
                    pawn._set_pos_Y(y)
                    self.list_pawn.append(pawn) #append pawns into a list to stock them and be able to use them later

                    # set settings of box as pawns
                    box = Box(self.list_box_owner[line][item], False)
                    box._set_pos_X(x)
                    box._set_pos_Y(y)
                    box._set_box_color(int(9))

                    self.list_box.append(box)

                else: #if there are no pawns on box :
                    box = Box(self.list_box_owner[line][item], True) #True means the box is empty
                    box._set_pos_X(x)
                    box._set_pos_Y(y)
                    box._set_box_color(int(9))
                    self.list_box.append(box)


    def draw_map(self, surface, color_liste, boolean_Select, posX, posY ):
        #That VAR permit MODULO to display grid
        line_box = 0
        item_box = 0

        #display the image for special box
        for em in range(len(self.list_box)):
            x = self.list_box[em]._get_pos_X()
            y = self.list_box[em]._get_pos_Y()
            if self.list_box[em].owner_box == 'player_one_fix' or self.list_box[em].owner_box == 'player_two_fix':
                appearance_box = pygame.image.load(self.list_box[em].image_box)
                surface.blit(appearance_box, (x, y))

        #display box
        for em in range(len(self.list_box)):
            x = BOARD_TOPLEFT[0] + item_box * (CELL_SIZE[0] + CELL_SPACING[0])
            y = BOARD_TOPLEFT[1] + line_box * (CELL_SIZE[1] + CELL_SPACING[1])
            pygame.draw.rect(surface, COLOR_LIST[self.list_box[em]._get_box_color()], (x, y, CELL_SIZE[0], CELL_SIZE[1]), 5)
            #box are stocked into a simple list, to deplay them as a grid, just used %
            item_box+=1
            if item_box % self.columns == 0:
                line_box+=1
                item_box=0

        #display pawns with their position X & Y
        for line_box in range(8):
            for item_box in range(10):
                x = BOARD_TOPLEFT[0] + item_box * (CELL_SIZE[0] + CELL_SPACING[0])
                y = BOARD_TOPLEFT[1] + line_box * (CELL_SIZE[1] + CELL_SPACING[1])
                for em in range(len(self.list_pawn)):
                    pawn_X = self.list_pawn[em]._get_pos_X()
                    pawn_Y = self.list_pawn[em]._get_pos_Y()
                    if pawn_X == x and pawn_Y == y:
                        appearance_pawn = pygame.image.load(self.list_pawn[em].image_pawn)
                        surface.blit(appearance_pawn, (x-20, y-114))


    def draw_signboard(self, surface, index_pawn):
        """Display signboards clockwise and counterclockwise"""
        if self.list_pawn[index_pawn].pawn_is_select:
            direction_clockwise = pygame.image.load("source/images/direction_clockwise.png")
            surface.blit(direction_clockwise, (window_size[0]//2 + 50, window_size[1] - 35))
            direction_counterclockwise = pygame.image.load("source/images/direction_counterclockwise.png")
            surface.blit(direction_counterclockwise, (window_size[0]//2 - 155, window_size[1] - 35))

    def where_we_clicked(self, position):
        """ It permits to save position and index of Box and Pawn where we clicked"""
        box_X = int()
        box_Y = int()
        pawn_X = int()
        pawn_Y = int()

        for line in range(8):
            for item in range(10):
                x = BOARD_TOPLEFT[0] + item * (CELL_SIZE[0] + CELL_SPACING[0])
                y = BOARD_TOPLEFT[1] + line * (CELL_SIZE[1] + CELL_SPACING[1])
                if x <= position[0] <= x + CELL_SIZE[0] and y <= position[1] <= y + CELL_SIZE[1]:
                    for index_box in range(len(self.list_box)):
                        box_X = self.list_box[index_box]._get_pos_X()
                        box_Y = self.list_box[index_box]._get_pos_Y()
                        if x == box_X and box_Y == y:
                            break
                    for index_pawn in range(len(self.list_pawn)):
                        pawn_X = self.list_pawn[index_pawn]._get_pos_X()
                        pawn_Y = self.list_pawn[index_pawn]._get_pos_Y()
                        if pawn_X == x and pawn_Y == y:
                            break

        return (box_X, box_Y, index_box, pawn_X, pawn_Y, index_pawn )
