# 2048

from game_2048 import *

commands = { "U" : "up", "L" : "left", "R" : "right", "D" : "down" }

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
    while not is_grid_over(grid) and grid_get_max_value(grid) < 2048:
        move = read_next_move()
        grid_move(grid, commands[move])
        grid_add_new_tile(grid)
        grid_print(grid)
    if grid_get_max_value(grid) == 2048:
        print("Vous avez gagné !!")
    else:
        print("Vous avez perdu...")
    print("Votre score est de "+str(grid_score(grid))+" points.")

if __name__ == '__main__':
    play()
    exit(1)
