# Module idle 2048

from game_2048 import *
import sys

commands = {"U": "up", "L": "left", "R": "right", "D": "down", "S":"save"}

def read_next_move():
    """
    Lit une nouvelle commande de l'utilisateur

    valeur renvoyée: (str) la direction à suivre pour grid_move()
    """
    move =  input('Your Move ? ((U)p, (D)own, (L)eft, (R)ight, (S)ave)').upper()
    while move not in commands:
        move = input('Your Move ? ((U)p, (D)own, (L)eft, (R)ight, (S)ave) ').upper()
    return move

def read_gridsize():
    """

    """
    number = input('What grid size do you want to play?')
    while int(number)<3 and 10<int(number):
        number = input('What grid size do you want to play?')
    return int(number)

def play():
    game = input ('Do you want to create a new game or load a game? ((C)harge, (N)ew)').upper()
    commande_new=['N', 'C']
    while game not in commande_new:
        game = input ('Do you want to create a new game or load a game?((C)harge, (N)ew) ').upper()
    if game == 'N':
        number=read_gridsize()
        grid = grid_init(number)
    elif game == 'C': 
        try:
            grid = grid_load("save")
            number=len(grid)
            print("Your grid is here!")
        except FileNotFoundError:
            print ("Oops! There is no save file")
            number=read_gridsize()
            grid = grid_init(number)
   
    grid_print(grid, number)
    # Arrêt si la grille est pleine ou aucun mouvements possibles
    while not is_grid_over(grid) or True in move_possible(grid):
        # Lecture de la direction souhaitée
        move = read_next_move()
        if move == "S":
            grid_save(grid,"save")
            print("Save done")
            sys.exit(1)
        new_grid  = grid_move(grid, commands[move])
        # Pas de déplacement dans la direction d donc on demande une autre direction
        if new_grid == grid:
            continue
        grid = new_grid
        # Ajout d'une nouvelle tuile
        grid_add_new_tile(grid)
        # Affichage de la grille
        grid_print(grid, number)
    if grid_get_max_value(grid) == 2048:
        print("Vous avez gagné !!")
    else:
        print("Vous avez perdu...")
    print("Votre score est de "+str(grid_score(grid))+" points.")

if __name__ == '__main__':
    play()
    exit(1)
