import pygame
from constantes import*
from Map import*
from Box import*

class Pawn:
    """Create Pawn object"""
    def __init__(self, name_pawn, owner_pawn, direction_pawn): #,direction_pawn):
        """Initialize attributs
        self.name_pawn = Pawn's name
        self.image_pawn = Pawn's image path
        self._pos_X = coordinate X
        self._pos_Y = coordinate Y
        self.pawn_is_select = boolean, pawns is select ?
        self.owner_pawn = owner of pawn
        self.pawn_is_alive : boolean, pawn still alive ?
        self.can_move = boolean, pawn can move ?
        """
        self.name_pawn = name_pawn
        self.direction_pawn = direction_pawn
        self.image_pawn = "source/images/{}_{}_{}.png".format(name_pawn, owner_pawn, direction_pawn)
        self._pos_X = int()
        self._pos_Y = int()
        self.pawn_is_select = False
        self.owner_pawn = owner_pawn
        self.pawn_is_alive = True
        self.can_move = True
        self.can_turn = True
        self.can_exchange_position = False
        self.accept_exchange_position = False
        self.return_laser = False
        self.list_direction_possible = ["north", "east", "south", "west"]


    def select_pawn(game_board, turn_player, index_player):
        """Function to select a pawn from Board"""
        position = pygame.mouse.get_pos()
        box_X, box_Y, index_box, pawn_X, pawn_Y, index_pawn = game_board.where_we_clicked(position)
        if game_board.list_box[index_box].box_is_empty: #if box is empty
            return (False, box_X, box_Y, 0, index_box) #Can't select, index_em = NULL
            #because no pawns here
        else: #if box is not empty
            game_board.list_pawn[index_pawn].pawn_is_select = True
            return (True, pawn_X, pawn_Y, index_pawn, index_box) #Can select a pawn, at x y coordinate
            # and his place in list is "em"



    def move_pawn(game_board,next_pawn_X,next_pawn_Y, index_pawn, old_index_box):
        """ Function to move a pawn from Board
            next_pawn_X & next_pawn_Y = Pawn new coordinates
            index_pawn = position of Pawn in list Pawn
            old_index_box = index in List box before move
        """
        box_X, box_Y, index_box = Box.find_index_box(game_board, next_pawn_X, next_pawn_Y)
        if game_board.list_box[index_box].check_owner_box(game_board, index_box, index_pawn) == True:
            if game_board.list_box[index_box].box_is_empty:
                #reset owner box to neutral after moving
                Box.change_owner_box(game_board, index_box, old_index_box)
                #new box wouldnt be empty anymore
                game_board.list_box[index_box].box_is_empty = False
                #last box would be empty
                game_board.list_box[old_index_box].box_is_empty = True
                #set new Pawn's coordinates
                game_board.list_pawn[index_pawn]._set_pos_X(next_pawn_X)
                game_board.list_pawn[index_pawn]._set_pos_Y(next_pawn_Y)
                #After moving, Pawn is not select anymore
                game_board.list_pawn[index_pawn].pawn_is_select = False
                #Whole box turn to Brown after Pawn's move
                for index_box in range(len(game_board.list_box)):
                    game_board.list_box[index_box]._set_box_color(9)
                    game_board.list_pawn[index_pawn].pawn_is_select = True
            else :
                #if box is not empty, check if the pawn on this box can exchange position
                can_exchange_position, index_next_pawn = Pawn.can_exchange_position(game_board, index_pawn, box_X, box_Y)
                if can_exchange_position:
                    Pawn.exchange_position(game_board, old_index_box ,index_pawn, index_next_pawn)
                    for index_box in range(len(game_board.list_box)):
                        game_board.list_box[index_box]._set_box_color(9)
                        game_board.list_pawn[index_pawn].pawn_is_select = False
                else: game_board.list_pawn[index_pawn].can_move = False
        else:
            game_board.list_pawn[index_pawn].can_move = False
        pygame.display.update()
        return index_pawn

    def change_direction_pawn(game_board, index_pawn, direction):
        list_possible_dir=['north','east','south','west']
        if direction == 'clockwise':
            i = 1
        else:
            i = -1
        for el in range(len(list_possible_dir)):
            if list_possible_dir[el] == game_board.list_pawn[index_pawn].direction_pawn and game_board.list_pawn[index_pawn].name_pawn != 'sphinx':
                next_dir = (el + i) % 4
                if next_dir < 0 : next_dir = 3
                break
            elif list_possible_dir[el] == game_board.list_pawn[index_pawn].direction_pawn and game_board.list_pawn[index_pawn].name_pawn == 'sphinx':
                if game_board.list_pawn[index_pawn].direction_pawn == "south" or game_board.list_pawn[index_pawn].direction_pawn == "north":
                    next_dir = (el + 3*i) % 4
                else: next_dir = (el + i) % 4
                break
        game_board.list_pawn[index_pawn].direction_pawn = list_possible_dir[next_dir]


    def can_exchange_position(game_board, index_pawn_select, box_X, box_Y):
        for el in range(len(game_board.list_pawn)):
            pawn_X = game_board.list_pawn[el]._get_pos_X()
            pawn_Y = game_board.list_pawn[el]._get_pos_Y()

            if  box_X == pawn_X and box_Y == pawn_Y:
                if game_board.list_pawn[index_pawn_select].can_exchange_position and game_board.list_pawn[el].accept_exchange_position:
                    index_next_pawn = el
                    return (True, index_next_pawn)
        return (False, 3)



    def exchange_position(game_board, index_box_select, index_pawn_select, index_next_pawn):

        coord_X = game_board.list_pawn[index_pawn_select]._get_pos_X()
        coord_Y = game_board.list_pawn[index_pawn_select]._get_pos_Y()

        game_board.list_pawn[index_pawn_select]._set_pos_X(game_board.list_pawn[index_next_pawn]._get_pos_X())
        game_board.list_pawn[index_pawn_select]._set_pos_Y(game_board.list_pawn[index_next_pawn]._get_pos_Y())

        game_board.list_pawn[index_next_pawn]._set_pos_X(coord_X)
        game_board.list_pawn[index_next_pawn]._set_pos_Y(coord_Y)


    def find_index_pawn(game_board, index_box):
        """find index_pawn with the index box"""
        box_X = game_board.list_box[index_box]._get_pos_X()
        box_Y = game_board.list_box[index_box]._get_pos_Y()
        for index_pawn in range(len(game_board.list_pawn)):
            pawn_X = game_board.list_pawn[index_pawn]._get_pos_X()
            pawn_Y = game_board.list_pawn[index_pawn]._get_pos_Y()
            if pawn_X == box_X and pawn_Y == box_Y:
                return (pawn_X, pawn_Y, index_pawn)


    def get_index_direction_pawn(self):
        list_direction = ['north','east','south','west']
        for index_direction in range(len(list_direction)):
            if self.direction_pawn == list_direction[index_direction]:
                return index_direction


    def _get_pos_X(self):
        """Méthode qui sera appelée quand on souhaitera
         accéder en lecture
                à l'attribut '_pos_X'"""
        return self._pos_X

    def _set_pos_X(self, new_pos_X):
        """Méthode appelée quand on souhaite modifier le lieu de résidence"""
        self._pos_X = new_pos_X

    def _get_pos_Y(self):
        """Méthode qui sera appelée quand on souhaitera accéder en lecture
                à l'attribut '_pos_X'"""
        return self._pos_Y

    def _set_pos_Y(self, new_pos_Y):
        """Méthode appelée quand on souhaite modifier le lieu de résidence"""
        self._pos_Y = new_pos_Y

    pos_X = property(_get_pos_X, _set_pos_X)
    pos_Y = property(_get_pos_Y, _set_pos_Y)


class Pharaoh(Pawn):
    def __init__(self, name_pawn, owner_pawn, direction_pawn):
        """Pharaoh statut, if he dies, the game is over"""
        Pawn.__init__(self, name_pawn, owner_pawn, direction_pawn)
        self.can_turn = False

    def is_hit(self, laser_shot,game_board, index_pawn, index_box):
        game_board.list_box[index_box].box_is_empty = True
        del game_board.list_pawn[index_pawn]
        game_board.end_game = True
        return 0


class Anubis(Pawn):
    """Create Anubis's pawn"""
    def __init__(self, name_pawn, owner_pawn, direction_pawn):
        Pawn.__init__(self, name_pawn, owner_pawn, direction_pawn)
        self.accept_exchange_position = True

    def is_hit(self, laser_shot,game_board, index_pawn, index_box):
        index_laser_shot = laser_shot.list_direction_possible.index(laser_shot.direction_laser)
        if self.direction_pawn == laser_shot.list_direction_possible[((index_laser_shot + 2) % 4)]:
            pass
        else:
            game_board.list_box[index_box].box_is_empty = True
            del game_board.list_pawn[index_pawn]

        return index_box



class Scarab(Pawn):
    def __init__(self, name_pawn, owner_pawn, direction_pawn):
        Pawn.__init__(self, name_pawn, owner_pawn, direction_pawn)
        self.can_exchange_position = True
        self.return_laser = True

    def is_hit(self, laser_shot,game_board, index_pawn, index_box):
        index_laser_shot = laser_shot.list_direction_possible.index(laser_shot.direction_laser)

        if self.direction_pawn == 'north' or self.direction_pawn == 'south':
            if laser_shot.direction_laser == 'north':
                index_box = index_box + 1
                laser_shot.direction_laser = 'east'

            elif laser_shot.direction_laser == 'south':
                index_box = index_box - 1
                laser_shot.direction_laser = 'west'

            elif laser_shot.direction_laser == 'west':
                index_box = index_box + 10
                laser_shot.direction_laser = 'south'

            elif laser_shot.direction_laser == 'east':
                index_box = index_box - 10
                laser_shot.direction_laser = 'north'


        elif self.direction_pawn == 'east' or self.direction_pawn == 'west':
            if laser_shot.direction_laser == 'north':
                index_box = index_box - 1
                laser_shot.direction_laser = 'west'

            elif laser_shot.direction_laser == 'south':
                index_box = index_box + 1
                laser_shot.direction_laser = 'east'

            elif laser_shot.direction_laser == 'west':
                index_box = index_box - 10
                laser_shot.direction_laser = 'north'

            elif laser_shot.direction_laser == 'east':
                index_box = index_box + 10
                laser_shot.direction_laser = 'south'
        return index_box

class Pyramid(Pawn):
    def __init__(self, name_pawn, owner_pawn, direction_pawn):
        Pawn.__init__(self, name_pawn, owner_pawn, direction_pawn)
        self.accept_exchange_position = True
        self.return_laser = True


    def is_hit(self, laser_shot,game_board, index_pawn, index_box):
        index_laser_shot = laser_shot.list_direction_possible.index(laser_shot.direction_laser)

        if self.direction_pawn == laser_shot.list_direction_possible[(index_laser_shot + 3) % 4]\
        or self.direction_pawn == laser_shot.list_direction_possible[(index_laser_shot) % 4]:

            if self.direction_pawn == 'south':
                if laser_shot.direction_laser == 'west':
                    index_box = index_box - 10
                    laser_shot.direction_laser = 'north'

                elif laser_shot.direction_laser == 'south':
                    index_box = index_box + 1
                    laser_shot.direction_laser = 'east'

            elif self.direction_pawn == 'east':
                if laser_shot.direction_laser == 'east':
                    index_box = index_box - 10
                    laser_shot.direction_laser = 'north'

                elif laser_shot.direction_laser == 'south':
                    index_box = index_box - 1
                    laser_shot.direction_laser = 'west'

            elif self.direction_pawn == 'north':
                if laser_shot.direction_laser == 'north':
                    index_box = index_box - 1
                    laser_shot.direction_laser = 'west'

                elif laser_shot.direction_laser == 'east':
                    index_box = index_box + 10
                    laser_shot.direction_laser = 'south'

            elif self.direction_pawn == 'west':
                if laser_shot.direction_laser == 'north':
                    index_box = index_box + 1
                    laser_shot.direction_laser = 'east'

                elif laser_shot.direction_laser == 'west':
                    index_box = index_box + 10
                    laser_shot.direction_laser = 'south'
        else:
            game_board.list_box[index_box].box_is_empty = True
            del game_board.list_pawn[index_pawn]
            return 0
        return index_box



class Sphinx(Pawn):
    def __init__(self, name_pawn, owner_pawn, direction_pawn):
        Pawn.__init__(self, name_pawn, owner_pawn, direction_pawn)
        self.can_move = False
        self.can_shoot = True

    def is_hit(self, laser_shot,game_board, index_pawn, index_box):
        return index_box
