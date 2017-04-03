# Module idle 2048

from game_2048 import *

commands = {"U": "up", "L": "left", "R": "right", "D": "down" }

def read_next_move():
    """
    Lit une nouvelle commande de l'utilisateur

    valeur renvoyée: (str) la direction à suivre pour grid_move()
    """
    move =  input('Your Move ? ((U)p, (D)own, (L)eft, (R)ight) ').upper()
    while move not in commands:
        move = input('Your Move ? ((U)p, (D)own, (L)eft, (R)ight) ').upper()
    return move

def play():
    grid = grid_init()
    grid_print(grid)
    # Arrêt si la grille est pleine ou aucun mouvements possibles
    while not is_grid_over(grid) or True in move_possible(grid):
        # Lecture de la direction souhaitée
        move = read_next_move()
        new_grid  = grid_move(grid, commands[move])
        # Pas de déplacement dans la direction d donc on demande une autre direction
        if new_grid == grid:
            continue
        grid = new_grid
        # Ajout d'une nouvelle tuile
        grid_add_new_tile(grid)
        # Affichage de la grille
        grid_print(grid)
    if grid_get_max_value(grid) == 2048:
        print("Vous avez gagné !!")
    else:
        print("Vous avez perdu...")
    print("Votre score est de "+str(grid_score(grid))+" points.")

if __name__ == '__main__':
    play()
    exit(1)
