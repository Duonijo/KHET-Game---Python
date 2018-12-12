import pygame
from pygame.locals import *
from constantes import *
from Map import*
from Box import*

class Laser:
    def __init__(self, direction_laser):
        self.direction_laser = direction_laser
        self.list_direction_possible = ["north", "east", "south", "west"]

    def automatic_shot(self, game_board, surface, index_shooter, next_index_box):
        box_X = int()
        box_Y = int()
        next_position = CELL_SIZE[0] + CELL_SPACING[0]
        if self.direction_laser == 'east':
            if game_board.list_box[next_index_box].box_is_empty:
                position_X  = game_board.list_pawn[index_shooter]._get_pos_X() + CELL_SIZE[0]
                position_Y = game_board.list_pawn[index_shooter]._get_pos_Y() + CELL_SIZE[0] // 2
                while game_board.list_box[next_index_box].box_is_empty:
                    Map.draw_map( game_board, surface, COLOR_LIST, False, 0, 0)
                    pygame.draw.line(surface, COLOR_LIST[1], (position_X, position_Y) , (position_X + next_position + CELL_SPACING[0], position_Y), 4)
                    next_index_box += 1
                    pygame.display.update()
                    if position_X > BOARD_TOPLEFT[0] + (CELL_SIZE[0] + CELL_SPACING[0]) * 8:
                        break

                    position_X += next_position
                    box_X = game_board.list_box[next_index_box]._get_pos_X()
                    box_Y = game_board.list_box[next_index_box]._get_pos_Y()

            else:
                position_X  = game_board.list_pawn[index_shooter]._get_pos_X() + CELL_SIZE[0]
                position_Y = game_board.list_pawn[index_shooter]._get_pos_Y() + CELL_SIZE[0] // 2
                pygame.draw.line(surface, COLOR_LIST[1], (position_X, position_Y) , (position_X, position_Y - CELL_SPACING[1]), 4)
                pygame.display.update()
                box_X = game_board.list_box[next_index_box]._get_pos_X()
                box_Y = game_board.list_box[next_index_box]._get_pos_Y()

        elif self.direction_laser == 'west':
            if game_board.list_box[next_index_box].box_is_empty:
                position_X  = game_board.list_pawn[index_shooter]._get_pos_X()
                position_Y = game_board.list_pawn[index_shooter]._get_pos_Y() + CELL_SIZE[0] // 2
                while game_board.list_box[next_index_box].box_is_empty:
                    Map.draw_map( game_board, surface, COLOR_LIST, False, 0, 0)
                    pygame.draw.line(surface, COLOR_LIST[1], (position_X, position_Y) , (position_X-next_position-CELL_SPACING[0], position_Y),4)
                    next_index_box -= 1
                    pygame.display.update()
                    position_X -= next_position

                    if position_X == BOARD_TOPLEFT[0]:
                        break
                    box_X = game_board.list_box[next_index_box]._get_pos_X()
                    box_Y = game_board.list_box[next_index_box]._get_pos_Y()

            else:
                position_X  = game_board.list_pawn[index_shooter]._get_pos_X()
                position_Y = game_board.list_pawn[index_shooter]._get_pos_Y() + CELL_SIZE[0] // 2
                pygame.draw.line(surface, COLOR_LIST[1], (position_X, position_Y) , (position_X, position_Y - CELL_SPACING[1]), 4)
                pygame.display.update()
                box_X = game_board.list_box[next_index_box]._get_pos_X()
                box_Y = game_board.list_box[next_index_box]._get_pos_Y()

        elif self.direction_laser == 'north':
            if game_board.list_box[next_index_box].box_is_empty:
                position_X  = game_board.list_pawn[index_shooter]._get_pos_X() + CELL_SIZE[0] // 2
                position_Y = game_board.list_pawn[index_shooter]._get_pos_Y()
                while game_board.list_box[next_index_box].box_is_empty:
                    Map.draw_map( game_board, surface, COLOR_LIST, False, 0, 0)
                    pygame.draw.line(surface, COLOR_LIST[1], (position_X, position_Y) , (position_X, position_Y - next_position - CELL_SPACING[0]), 4)
                    next_index_box -= 10
                    pygame.display.update()
                    if next_index_box < 0:
                        break
                    position_Y -= next_position
                    box_X = game_board.list_box[next_index_box]._get_pos_X()
                    box_Y = game_board.list_box[next_index_box]._get_pos_Y()
            else:
                position_X  = game_board.list_pawn[index_shooter]._get_pos_X() + CELL_SIZE[0] // 4
                position_Y = game_board.list_pawn[index_shooter]._get_pos_Y()
                pygame.draw.line(surface, COLOR_LIST[1], (position_X, position_Y) , (position_X, position_Y - CELL_SPACING[1]), 4)
                pygame.display.update()
                box_X = game_board.list_box[next_index_box]._get_pos_X()
                box_Y = game_board.list_box[next_index_box]._get_pos_Y()

        elif self.direction_laser == 'south':
            if game_board.list_box[next_index_box].box_is_empty:
                position_X  = game_board.list_pawn[index_shooter]._get_pos_X() + CELL_SIZE[0]//2
                position_Y = game_board.list_pawn[index_shooter]._get_pos_Y() + CELL_SIZE[0]
                while game_board.list_box[next_index_box].box_is_empty:
                    Map.draw_map( game_board, surface, COLOR_LIST, False, 0, 0)
                    pygame.draw.line(surface, COLOR_LIST[1], (position_X, position_Y) , (position_X, position_Y + next_position + CELL_SPACING[0]), 4)
                    next_index_box += 10
                    pygame.display.update()
                    if next_index_box > 79:
                        break
                    position_Y += next_position
                    box_X = game_board.list_box[next_index_box]._get_pos_X()
                    box_Y = game_board.list_box[next_index_box]._get_pos_Y()

            else:
                position_X  = game_board.list_pawn[index_shooter]._get_pos_X() + CELL_SIZE[0]//2
                position_Y = game_board.list_pawn[index_shooter]._get_pos_Y() + CELL_SIZE[0]
                pygame.draw.line(surface, COLOR_LIST[1], (position_X, position_Y) , (position_X, position_Y + CELL_SPACING[1]), 4)
                pygame.display.update()
                box_X = game_board.list_box[next_index_box]._get_pos_X()
                box_Y = game_board.list_box[next_index_box]._get_pos_Y()


        for index_pawn in range(len(game_board.list_pawn)-1):
            pawn_X = game_board.list_pawn[index_pawn]._get_pos_X()
            pawn_Y = game_board.list_pawn[index_pawn]._get_pos_Y()
            if pawn_X == box_X and pawn_Y == box_Y:
                print("index pawn : 0 : ", index_pawn)
                next_index_box = game_board.list_pawn[index_pawn].is_hit(self, game_board, index_pawn, next_index_box)
                if next_index_box == 0:
                    break

                if game_board.list_pawn[index_pawn].return_laser:
                    self.automatic_shot(game_board, surface, index_pawn, next_index_box)

        pygame.time.delay(500)
