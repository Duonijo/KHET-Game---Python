from constantes import*
from Map import*

def newBoard(n,m,player): #Elle retourne une liste à deux dimensions représentant l’état initial d’un plateau de jeu à
    '''
    :param n:  n lignes
    :param m: m  colonne
    '''

    board = [[[0] * m for i in range(n)], [ [0] * m for i in range(n)]] # Créer une lsite à deux dimensions, 1e pour les jours, 2nd pour le nb pions

    return board


def turnPlayer(player, player_max): #Changement tour du joueur
    if player <  player_max:
        player+=1
                 
    elif player== player_max:
        player=1
    return player


def possible(gameBoard,n,m,player,position): #Verifie la possiblité de cliquer sur une case
    
    for line in range(n):
        for item in range(m):
            x = BOARD_TOPLEFT[0] + item * (CELL_SIZE[0] + CELL_SPACING[0])   #Colonne du tableau
            y = BOARD_TOPLEFT[1] + line * (CELL_SIZE[1] + CELL_SPACING[1])   #Ligne du tableau
            if x <= position[0] <= x + CELL_SIZE[0] and y <= position[1] <= y + CELL_SIZE[1]:
                if gameBoard[0][line][item] != 0 and gameBoard[0][line][item] != player:#Verifie si la case appartient au joueur
                    return False #Si on ne peut pas poser de pions, retourne False
    return True #On peut poser un pion


def pionSelect(n, m, position):  # Verifie la possiblité de cliquer sur une case

    for line in range(n):
        for item in range(m):
            x = BOARD_TOPLEFT[0] + item * (CELL_SIZE[0] + CELL_SPACING[0])  # Colonne du tableau
            y = BOARD_TOPLEFT[1] + line * (CELL_SIZE[1] + CELL_SPACING[1])  # Ligne du tableau
            if x <= position[0] <= x + CELL_SIZE[0] and y <= position[1] <= y + CELL_SIZE[1]:
                    return True,x,y  # Si on ne peut pas poser de pions, retourne False
    return False  # On peut poser un pion

