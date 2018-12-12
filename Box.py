import pygame
from constantes import*
from Pawn import*


class Box:
    """Création objets box"""
    def __init__(self, owner_box, box_is_empty):
        """Initialize attributs"""
        self.owner_box = owner_box
        self.image_box = "source/images/{}.png".format(owner_box)
        self._pos_X = int()
        self._pos_Y = int()
        self.box_is_empty = box_is_empty
        self._box_color = int()


    def color_box_pawn_select(game_board, pawn_X, pawn_Y, index_pawn):
        """Color box in range of moving pawn"""
        box_X, box_Y, index_box = Box.find_index_box(game_board, pawn_X, pawn_Y)
        box_min_X = game_board.list_box[index_box]._get_pos_X() - 1 * (CELL_SIZE[0] + CELL_SPACING[0])
        box_min_Y = game_board.list_box[index_box]._get_pos_Y() - 1 * (CELL_SIZE[0] + CELL_SPACING[0])
        el = index_box

        for line in range(3):
            for item in range(3):
                x = box_min_X + item * (CELL_SIZE[0] + CELL_SPACING[0])
                y = box_min_Y + line * (CELL_SIZE[1] + CELL_SPACING[1])
                #Limits range boxes adjacents
                if BOARD_TOPLEFT[1] > y or  y >  BOARD_TOPLEFT[1] + 7 * (CELL_SIZE[1] + CELL_SPACING[1])\
                 or BOARD_TOPLEFT[0] > x or x > BOARD_TOPLEFT[0] + 9 * (CELL_SIZE[0] + CELL_SPACING[0]):
                    continue
                box_X, box_Y, index_Box = Box.find_index_box(game_board, x, y)
                if game_board.list_box[index_Box].box_is_empty ==  False: #if there are a pawn
                    for em in range(len(game_board.list_pawn)):
                        pawn_X = game_board.list_pawn[em]._get_pos_X()
                        pawn_Y = game_board.list_pawn[em]._get_pos_Y()
                        if  x == pawn_X and y == pawn_Y:
                            #if pawn can swap position
                            if game_board.list_pawn[index_pawn].can_exchange_position and \
                            game_board.list_pawn[em].accept_exchange_position:
                                game_board.list_box[index_Box]._set_box_color(5)
                            else:
                                #color box as a box busy (RED)
                                game_board.list_box[index_Box]._set_box_color(2)
                else: game_board.list_box[index_Box]._set_box_color(3)
                game_board.list_box[index_box]._set_box_color(1)
        return index_box


    def box_in_range(game_board, index_box):
        """Check if the new position is in the range of moving from selected pawn"""
        position = pygame.mouse.get_pos()
        box_min_X = game_board.list_box[index_box]._get_pos_X() - 1 * (CELL_SIZE[0] + CELL_SPACING[0])
        box_max_X = game_board.list_box[index_box]._get_pos_X() + 2 * (CELL_SIZE[0] + CELL_SPACING[0])
        box_min_Y = game_board.list_box[index_box]._get_pos_Y() - 1 * (CELL_SIZE[0] + CELL_SPACING[0])
        box_max_Y = game_board.list_box[index_box]._get_pos_Y() + 2 * (CELL_SIZE[0] + CELL_SPACING[0])

        for line in range(8):
            for item in range(10):
                x = BOARD_TOPLEFT[0] + item * (CELL_SIZE[0] + CELL_SPACING[0])
                y = BOARD_TOPLEFT[1] + line * (CELL_SIZE[1] + CELL_SPACING[1])
                if x <= position[0] <= x + CELL_SIZE[0] and y <= position[1] <= y + CELL_SIZE[1]:
                    if (position[0] >= box_min_X  and position[0] <= box_max_X
                        and position[1] <= box_max_Y and position[1] >= box_min_Y):
                        return True
        return False


    def check_owner_box(self,game_board,index_box, index_pawn):
        """Return True if player try to move on his own box, return False else"""
        if game_board.list_pawn[index_pawn].owner_pawn == "player_one" and game_board.list_box[index_box].owner_box != "player_two_fix":
            return True
        elif game_board.list_pawn[index_pawn].owner_pawn == "player_two" and game_board.list_box[index_box].owner_box != "player_one_fix":
            return True

        else: return False


    def change_owner_box(game_board,index_box, old_index_box):
        """After moving, reset owner of old and new box"""
        if game_board.list_box[old_index_box].owner_box == "player_one":
            game_board.list_box[old_index_box].owner_box = "neutral"
            game_board.list_box[index_box].owner_box = "player_one"
        elif game_board.list_box[old_index_box].owner_box == "player_two":
            game_board.list_box[old_index_box].owner_box = "neutral"
            game_board.list_box[index_box].owner_box = "player_two"


    def find_index_box(game_board, x, y):
        """ fin box'index with her coordinates
            -return : coordinates and box's index """
        for index_box in range(len(game_board.list_box)):
            box_X = game_board.list_box[index_box]._get_pos_X()
            box_Y = game_board.list_box[index_box]._get_pos_Y()
            if x == box_X and box_Y == y:
                return(box_X, box_Y, index_box)


    def _set_box_color(self, new_box_color):
        """Called Method when we set color"""
        self._box_color = new_box_color
        return new_box_color

    def _get_box_color(self):
        """Called Method when we get color"""
        return self._box_color

    def _get_pos_X(self):
        """Called Method when we get box's position X """
        return self._pos_X

    def _set_pos_X(self, new_pos_X):
        """Called Method when we set box's position X """
        self._pos_X = new_pos_X

    def _get_pos_Y(self):
        """Called Method when we get box's position Y """
        return self._pos_Y

    def _set_pos_Y(self, new_pos_Y):
        """Called Method when we set box's position Y """
        self._pos_Y = new_pos_Y

    pos_X = property(_get_pos_X, _set_pos_X)
    pos_Y = property(_get_pos_Y, _set_pos_Y)
    box_color = property(_get_box_color, _set_box_color)
