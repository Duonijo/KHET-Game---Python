import pygame
from pygame.locals import *
from Menu import*
from Laser import*
from Editor import*
from algorithms import*
from constantes import *
from SelectMap import*

pygame.init()


#Ouverture de la fenêtre Pygame (carré : largeur = hauteur)
fenetre = pygame.display.set_mode(window_size)
fenetre_menu = pygame.display.set_mode(window_size)
fenetre_editor = pygame.display.set_mode(window_size)
#Icone
#icone = pygame.image.load('icon.png').convert_alpha()
#pygame.display.set_icon(icone)

#Titre
pygame.display.set_caption(window_title)

# Rafraîchissement de l'écran
pygame.display.flip()
#musique
pygame.mixer.music.load("source/music/KHET_song.ogg")
pygame.mixer.music.play()
boolean_Generate = False
continuer = 1
posX=int()
posY=int()
box_X = int()
box_Y = int()
boolean_Select = False #Boolean, pawn is select?
boolean_Select_Editor = False#Boolean, pawn is select?
boolean_Select_Starter = False#Boolean, starter pawn is select?
menu = 1
game = 0
again = 0
editor = 0
select_map = 0
game_menu = Menu()
index_player = 0
list_player = ["player_one", "player_two"]
next_Round = False
index_pawn = int()

while continuer:

    while menu:

        for event in pygame.event.get():
            if event.type == QUIT:
                menu = 0
        if event.type == MOUSEBUTTONUP:
            position = pygame.mouse.get_pos()
            if game_menu.change_map(position):
                pygame.display.update()
            if game_menu.start_game(position):
                menu = 0
                game = 1
                game_board = Map(game_menu.list_map[game_menu.index_map])#map basic
                liste_name_pawn = game_board.generate_list_name() #name's pawn list
                list_box_owner = game_board.generate_list_owner()#owner box list
                list_direction_pawn = game_board.generate_list_direction()
                game_board.generate_map(fenetre,COLOR_LIST, list_box_owner)#Generate the map

            if game_menu.start_editor(position):
                menu = 0
                editor = 1
                game_board_edit = Editor()
                game_board_edit.starter_pawn(fenetre_editor)
                game_board_edit.generate_map(fenetre_editor, COLOR_LIST)

        if event.type == MOUSEMOTION:
            position = pygame.mouse.get_pos()
            game_menu.display_menu(fenetre_menu)
            if game_menu.start_game(position):
                game_menu.hand_cursor(position, fenetre_menu)
                pygame.mouse.set_visible(0)
            else :
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                pygame.mouse.set_visible(1)

        pygame.display.flip()


    while editor :
        pygame.mouse.set_visible(1)
        for event in pygame.event.get():
            if event.type == QUIT:
                menu = 1
                editor = 0

            if event.type == MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                for line_box in range(0,5):
                    for item_box in range(1):
                        x = BOARD_STARTER_TOPLEFT_EDITOR[0] + item_box * (CELL_SIZE[0] + CELL_SPACING_EDITOR[0])
                        y = BOARD_STARTER_TOPLEFT_EDITOR[1] + line_box * (CELL_SIZE[1] + CELL_SPACING_EDITOR[1])

                        if x <= position[0] <= x + CELL_SIZE[0] and y <= position[1] <= y + CELL_SIZE[1]:
                            if boolean_Select_Starter == False:
                                boolean_Select_Starter, posX, posY, index_box, index_pawn_starter = game_board_edit.select_pawn_editor(fenetre_editor)
                                print("'true'")
                                game_board_edit.list_starter_box[index_box]._set_box_color(4)
                                boolean_Select_Starter = True
                                box_X = x
                                box_Y = y
                                boolean_Select_Editor = True

                            else:
                                if box_X < position[0] < box_X + CELL_SIZE[0] and box_Y <= position[1] <= box_Y + CELL_SIZE[1]:
                                    game_board_edit.list_starter_box[index_box]._set_box_color(9)
                                    boolean_Select_Starter = False

                #box_X, box_Y, index_box, pawn_X, pawn_Y, index_pawn = game_board_edit.where_we_clicked(position)
                for line_box in range(8):
                    for item_box in range(10):
                        x = BOARD_TOPLEFT_EDITOR[0] + item_box * (CELL_SIZE[0] + CELL_SPACING[0])
                        y = BOARD_TOPLEFT_EDITOR[1] + line_box * (CELL_SIZE[1] + CELL_SPACING[1])
                        if x <= position[0] <= x + CELL_SIZE[0] and y <= position[1] <= y + CELL_SIZE[1]:
                            for em in range(len( game_board_edit.list_box_editor)):

                                editor_box_X =  game_board_edit.list_box_editor[em]._get_pos_X()
                                editor_box_Y =  game_board_edit.list_box_editor[em]._get_pos_Y()
                                if x == editor_box_X and y == editor_box_Y: #For box at coord = click
                                    if boolean_Select_Starter == True:
                                        if game_board_edit.list_box_editor[em].box_is_empty:
                                            name_pawn = game_board_edit.list_starter_pawn[1][index_pawn_starter].name_pawn
                                            owner_pawn = game_board_edit.list_starter_pawn[1][index_pawn_starter].owner_pawn
                                            direction_pawn = game_board_edit.list_starter_pawn[1][index_pawn_starter].direction_pawn
                                            if name_pawn == 'pharaoh' :
                                                pawn = Pharaoh(name_pawn, owner_pawn, direction_pawn)
                                            elif name_pawn == 'anubis' :
                                                pawn = Anubis(name_pawn, owner_pawn, direction_pawn)
                                            elif name_pawn == 'scarab' :
                                                pawn = Scarab(name_pawn, owner_pawn, direction_pawn)
                                            elif name_pawn == 'pyramid' :
                                                pawn = Pyramid(name_pawn, owner_pawn, direction_pawn)
                                            elif name_pawn == 'sphinx' :
                                                pawn = Sphinx(name_pawn, owner_pawn, direction_pawn)
                                            pawn._set_pos_X(x)
                                            pawn._set_pos_Y(y)
                                            if game_board_edit.list_box_editor[em].owner_box == 'neutral':
                                                game_board_edit.list_box_editor[em].owner_box = 'player_one'
                                            game_board_edit.list_box_editor[em].box_is_empty = False
                                            game_board_edit.list_pawn.append(pawn)
                                            index_pawn = len(game_board_edit.list_pawn)-1
                                    else:
                                        for el in range(len(game_board_edit.list_box_editor)):
                                            editor_box_X = game_board_edit.list_box_editor[el]._get_pos_X()
                                            editor_box_Y = game_board_edit.list_box_editor[el]._get_pos_Y()
                                            if x == editor_box_X and y == editor_box_Y:
                                                game_board_edit.list_box_editor[el]._set_box_color(4)
                                                #game_board_edit.list_box_editor[el].box_is_empty = False
                                                boolean_Select_Editor = True
                                                break
                        elif 992 <= position[0] <= 1250 and 32 <= position[1] <= 107:
                            editor=0
                            select_map = 1
                            board_select_map = SelectMap()
                            break
                        elif 615 <= position[0] <= 615 + game_board_edit.button_map_size[0] and 622 <= position[1] <= 622 + game_board_edit.button_map_size[1]:
                            boolean_Generate = True
                        elif  600 <= position[1] :
                            if  boolean_Select_Starter == False and boolean_Select_Editor == True:
                                        index_pawn = game_board_edit.edit_attributs_pawn(el)
                                        game_board_edit.settings_pawn( position, index_pawn, el)
                                        game_board_edit.list_box_editor[el]._set_box_color(9)

        if boolean_Generate == True:
            game_board_edit.generate_file_custom_map()
            boolean_Generate = False

        game_board_edit.draw_map(fenetre_editor)
        pygame.display.flip()
        pygame.display.update()



    while select_map:

        for event in pygame.event.get():
            if event.type == QUIT:
                select_map = 0
            if event.type == MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                print("click : ", len(game_board_edit.list_custom_map))
                game_board_edit.search_number_custom_map()
                boolean_Max = game_board_edit.max_map()
                #game_board_edit.search_number_custom_map()
                for line_box in range(len(game_board_edit.list_custom_map)):
                    for item_box in range(1):
                        x = BOARD_TOPLEFT[0]*2 + item_box * (CELL_SIZE[0] + CELL_SPACING[0])
                        y = BOARD_TOPLEFT[1] + line_box * (CELL_SIZE[1] + CELL_SPACING[1])
                        if x <= position[0] <= x +  CELL_SIZE[0]*5 + 20 and y <= position[1] <= y + CELL_SIZE[1]//1.7:
                            print("okkkkk")
                            game_board_edit.search_number_custom_map()
                            list_custom_pawn, list_custom_box = game_board_edit.start_custom_game(line_box, boolean_Max)
                            list_name_pawn = []
                            list_direction_pawn = []
                            list_box_owner = []

                            test = True
                            game_board = Map('classic')#map basic
                            for i in range(len(list_custom_pawn)):
                                pawn_Y = list_custom_pawn[i]._get_pos_Y()
                                list_custom_pawn[i]._set_pos_Y(pawn_Y + 110)
                                game_board.list_pawn.append(list_custom_pawn[i])

                            for i in range(len(list_custom_box)):
                                box_Y = list_custom_box[i]._get_pos_Y()
                                list_custom_box[i]._set_pos_Y(box_Y + 110)
                                game_board.list_box.append(list_custom_box[i])
                            select_map = 0
                            game = 1
                            break

        #fenetre_editor.fill((255,255,255))
        board_select_map.display_select_map(fenetre_editor)
        board_select_map.select_map(fenetre_editor)

        pygame.display.update()

    while game:
        pygame.mouse.set_visible(1)
        for event in pygame.event.get():
            if event.type == QUIT:
                game = 0
                again = 0
                continuer = 0
                #To know if player clicked on a box
            if event.type == MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                #To know if player clicked on a box
                for line in range(0,8):
                    for item in range(0,10):
                        x = BOARD_TOPLEFT[0] + item * (CELL_SIZE[0] + CELL_SPACING[0])
                        y = BOARD_TOPLEFT[1] + line * (CELL_SIZE[1] + CELL_SPACING[1])

                        if x <= position[0] <= x + CELL_SIZE[0] and y <= position[1] <= y + CELL_SIZE[1]:
                            if boolean_Select: #Select Loop
                                if box_X <= position[0] <= box_X + CELL_SIZE[0] and box_Y <= position[1] <= box_Y + CELL_SIZE[1]:
                                    game_board.list_pawn[index_pawn].pawn_is_select = False
                                    boolean_Select = False # no more pawn select
                                    for el in range(len(game_board.list_box)):
                                        game_board.list_box[el]._set_box_color(9) #put color back to brown for the board
                                    break
                                else:
                                    if Box.box_in_range(game_board, index_box): #if he clicked on an box in range
                                        index_pawn = Pawn.move_pawn(game_board,x, y, index_pawn, old_index_box) #Piob would move_pawn*
                                        if game_board.list_pawn[index_pawn].can_move: #if pawn select can move*
                                            """ index_pawn =  index pawn in list
                                                x & y = coordonate of new box after move
                                            """
                                            #next turn, laser will shot
                                            next_Round = True
                                            box_X = 0
                                            box_Y = 0
                                            # no more pawn select
                                            game_board.list_pawn[index_pawn].pawn_is_select = False
                                            boolean_Select = False
                                            #next player
                                            index_player = 0 if index_player == 1 else 1
                                            pygame.display.update()

                                        else:
                                            #pawn couldnt move on the last box, but reset his capcity to move to an another box
                                            game_board.list_pawn[index_pawn].can_move = True
                            else: #our select loop is false
                                #select a pawn
                                boolean_Select, posX, posY, index_pawn, index_box = Pawn.select_pawn(game_board, list_player, index_player)
                                if list_player[index_player] != game_board.list_pawn[index_pawn].owner_pawn: # can't select an ennemy pawn
                                     boolean_Select = False
                                if boolean_Select:
                                    if game_board.list_pawn[index_pawn].can_move:#color box only if pawn can move
                                        if game_board.list_pawn[index_pawn].pawn_is_select:
                                            index_box = Box.color_box_pawn_select(game_board, posX, posY,index_pawn)
                                            old_index_box = index_box #duplicate index_box as the old_index after moving

                        elif window_size[0]//2 - 155 <= position[0] <= window_size[0]//2 + 155 and window_size[1] - 35 <= position[1] <= window_size[1] - 5:
                            """ If we clicked on botside to change pawn's direction"""
                            if boolean_Select:
                                index_player = 0 if index_player == 1 else 1 #change direction change turn player aswell
                                if window_size[0]//2 + 50 <= position[0] <= window_size[0]//2 + 155:
                                    Pawn.change_direction_pawn(game_board, index_pawn, 'clockwise')

                                elif window_size[0]//2 - 155 <= position[0] <= window_size[0]//2 - 50:
                                    Pawn.change_direction_pawn(game_board, index_pawn, 'counterclockwise')
                                #relaod new informations about pawn
                                game_board.list_pawn[index_pawn].image_pawn = "source/images/{}_{}_{}.png".format(game_board.list_pawn[index_pawn].name_pawn,
                                game_board.list_pawn[index_pawn].owner_pawn, game_board.list_pawn[index_pawn].direction_pawn)

                                for el in range(len(game_board.list_box)):
                                    game_board.list_box[el]._set_box_color(9) #put color back to blue for the board
                                game_board.list_pawn[index_pawn].pawn_is_select = False
                                boolean_Select = False
                                next_Round = True

        """Game Loop"""
        game_background = pygame.image.load("source/images/game_background.png").convert()
        fenetre.blit(game_background, (0, 0))
        Map.draw_map( game_board, fenetre, COLOR_LIST, boolean_Select, posX, posY) #generate map
        for el in range(len(game_board.list_pawn)):
            if game_board.list_pawn[el].name_pawn == "pharaoh":
                if game_board.end_game == True:
                    game = 0
                    again = 1

        if boolean_Select:
            #display signboard to change pawn's direction if a pawn is select
            game_board.draw_signboard(fenetre, index_pawn)
            box_X, box_Y, index_box = Box.find_index_box(game_board, posX, posY)
        pygame.display.update()

        if next_Round == True: #end turn, shot a laser autimaticaly
            if index_player == 1:
                laser_shot = Laser(game_board.list_pawn[0].direction_pawn)#first direction of laser is the same as sphinx of player
                pygame.time.delay(500)
                if laser_shot.direction_laser == 'east' :
                    laser_shot.automatic_shot(game_board, fenetre, 0, 1)
                elif laser_shot.direction_laser == 'south':
                    laser_shot.automatic_shot(game_board, fenetre, 0, 10) #shot a laser
            else :
                laser_shot = Laser(game_board.list_pawn[len(game_board.list_pawn)-1].direction_pawn)
                if laser_shot.direction_laser == 'north' :
                    laser_shot.automatic_shot(game_board, fenetre, len(game_board.list_pawn)-1, 69)
                elif laser_shot.direction_laser == 'west':
                    laser_shot.automatic_shot(game_board, fenetre, len(game_board.list_pawn)-1, 78) #shot a laser
                    pygame.time.delay(500)
            next_Round = False #effect during end of turn is over


    while again:
        for event in pygame.event.get():
            if event.type == QUIT:
                again = 0
            if event.type == MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                if game_menu.change_map(position):
                    pygame.display.update()

                if game_menu.start_game(position):
                    again = 0
                    game = 1
                    game_board = Map(game_menu.list_map[game_menu.index_map])#map basic
                    liste_name_pawn = game_board.generate_list_name() #name's pawn list
                    list_box_owner = game_board.generate_list_owner()#owner box list
                    list_direction_pawn = game_board.generate_list_direction()
                    game_board.generate_map(fenetre,COLOR_LIST, list_box_owner)#Generate the map

        background = pygame.image.load("source/images/button_play_again.png")
        fenetre.blit(background, (0, 0))
        pygame.display.update()

pygame.quit()
