# Module idle 2048

from game_2048 import *
import sys

COMMANDS = {"U": "up", "L": "left", "R": "right", "D": "down", "S": "save"}
ALL_THEMES = {"0": DEFAULT, "1": CHEMISTRY}

def read_next_move():
    """
    Lit une nouvelle commande de l'utilisateur

    valeur renvoyée: (str) la direction à suivre pour grid_move()
    """
    move =  input('Your Move ? ((U)p, (D)own, (L)eft, (R)ight, (S)ave) ').upper()
    while move not in COMMANDS:
        move = input('Your Move ? ((U)p, (D)own, (L)eft, (R)ight, (S)ave) ').upper()
    return move

def read_gridsize():
    """
    Lit la taille de la grille demandée par l'utilisateur

    valeur renvoyée: (int) la taille de la grille
    """
    number = input('What grid size do you want to play? (between 3 and 10) ')
    while int(number) < 3 and int(number) > 10:
        number = input('What grid size do you want to play? (between 3 and 10) ')
    return int(number)

def read_theme():
    """
    Lit le theme demandée par l'utilisateur

    valeur renvoyée: (str) l'identifiant du theme
    """
    theme = input('What grid theme do you want? ((0)Default theme, (1)Chemistry theme) ')
    while theme not in ALL_THEMES:
        theme = input('What grid theme do you want? ((0)Default theme, (1)Chemistry theme) ')
    return theme
    

def play():
    game = input('Do you want to create a new game or load a game? ((C)harge, (N)ew) ').upper()
    commande_new = ['N', 'C']
    while game not in commande_new:
        game = input('Do you want to create a new game or load a game? ((C)harge, (N)ew) ').upper()
    if game == 'N':
        number = read_gridsize()
        grid = grid_init(number)
        theme = ALL_THEMES[read_theme()]
    elif game == 'C': 
        try:
            grid = grid_load("save")
            number = len(grid)
            theme = ALL_THEMES[read_theme()]
            print("Your save was successfully load")
        except FileNotFoundError:
            print("Oops! There is no save file")
            number = read_gridsize()
            theme = ALL_THEMES[read_theme()]
            grid = grid_init(number)
    grid_print(grid, number, theme)
    # Arrêt si la grille est pleine ou aucun mouvements possibles
    while not is_grid_over(grid) or True in move_possible(grid):
        # Lecture de la direction souhaitée
        move = read_next_move()
        if move == "S":
            grid_save(grid,"save")
            print("Save done")
            sys.exit(1)
        new_grid  = grid_move(grid, COMMANDS[move])
        # Pas de déplacement dans la direction d donc on demande une autre direction
        if new_grid == grid:
            continue
        grid = new_grid
        # Ajout d'une nouvelle tuile
        grid_add_new_tile(grid)
        # Affichage de la grille
        grid_print(grid, number, theme)
    if grid_get_max_value(grid) == 2048:
        print("You win !!")
    else:
        print("You lose...")
    print("Your score is "+str(grid_score(grid)))

if __name__ == '__main__':
    play()
    exit(1)
