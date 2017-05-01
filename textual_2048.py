from game_2048 import *
import time
from os import remove
from ai_2048 import *

COMMANDS = {"U": "up", "L": "left", "R": "right", "D": "down", "S": "save", "B": "back", "H": "hint"}

def read_next_move():
    """
    Lit une nouvelle commande de l'utilisateur

    valeur renvoyée: (str) la direction à suivre pour grid_move()
    """
    move =  input('Your Move ? ((U)p, (D)own, (L)eft, (R)ight, (S)ave, (B)ack, (H)int) ').upper()
    while move not in COMMANDS:
        move = input('Your Move ? ((U)p, (D)own, (L)eft, (R)ight, (S)ave, (B)ack, (H)int) ').upper()
    return move

def read_gridsize():
    """
    Lit la taille de la grille demandée par l'utilisateur

    valeur renvoyée: (int) la taille de la grille
    """
    number = input('What grid size do you want to play? (between 3 and 10) ')
    while int(number) < 3 or 10 < int(number):
        number = input('What grid size do you want to play? (between 3 and 10) ')
    return int(number)

def read_theme():
    """
    Lit le theme demandée par l'utilisateur

    valeur renvoyée: (str) l'identifiant du theme
    """
    theme = input('What grid theme do you want? ((0)Default, (1)Chemistry, (2)Alphabet) ')
    while theme not in THEMES:
        theme = input('What grid theme do you want? ((0)Default, (1)Chemistry, (2)Alphabet) ')
    return theme

def autoplay():
    """
    Lancement de la partie avec l'ordinateur qui joue à la place du joueur
    """
    n = read_gridsize()
    theme = THEMES[read_theme()]
    grid = grid_init(n)
    while not is_grid_over(grid) or True in move_possible(grid):
        # Evaluation de la grille
        move, evaluation = grid_max(grid)
        # Application de l'evaluation
        grid = grid_move(grid, move)
        # Ajout d'une nouvelle tuile
        grid_add_new_tile(grid)
        # Affichage de la grille et du mouvement effectue
        print(move)
        grid_print(grid, n, theme)
        # Pause de 700ms
        time.sleep(0.7)
    if grid_get_max_value(grid) >= 2048:
        print("Computer won !")
    else:
        print("Computer lose !")
    print("Score is "+str(grid_score(grid)))
    print("Please restart the program to play a new game")

def play():
    """
    Lancement de la partie
    """
    last_grid = None
    undo = 2
    hint = 2
    game = input('Do you want to create a new game or load a game? ((L)oad, (N)ew, (V)iew Leaderboard, (C)omputer play) ').upper()
    commande_new = ['N', 'L', 'V', 'C']
    while game not in commande_new:
        game = input('Do you want to create a new game or load a game? ((L)oad, (N)ew, (V)iew Leaderboard, (C)omputer play) ').upper()
    # Affichage du classement
    while game == 'V':
        liste = get_leaderboard("leaderboard")
        print("Leaderboard:")
        for score, name, size in liste:
            print(name+" - Score "+str(score)+" - Grille "+str(size)+"x"+str(size))
        game = input('Do you want to create a new game or load a game? ((L)oad, (N)ew, (V)iew Leaderboard, (C)omputer play) ').upper()
    # Nouvelle partie
    if game == 'N':
        number = read_gridsize()
        grid = grid_init(number)
        theme = THEMES[read_theme()]
    # Gestion de la partie sauvegardée
    elif game == 'L': 
        try:
            grid = grid_load("save")
            number = len(grid)
            theme = THEMES[read_theme()]
            print("Your game was successfully load")
            remove("save")
        except FileNotFoundError:
            print("Oops! There is no save file, a new game will start")
            number = read_gridsize()
            theme = THEMES[read_theme()]
            grid = grid_init(number)
    elif game == "C":
        autoplay()
        exit(1)
    pseudo = input("What is your pseudo ? ")
    grid_print(grid, number, theme)
    # Arrêt si la grille est pleine ou aucun mouvement possible
    while not is_grid_over(grid) or True in move_possible(grid):
        # Lecture de la direction souhaitée
        move = read_next_move()
        # Sauvegarde de la partie
        if move == "S":
            grid_save(grid,"save")
            print("Save done")
            exit(1)
        # Retour arrière
        elif move == "B":
            if last_grid is not None and last_grid != grid:
                if undo > 0:
                    undo -= 1
                    grid = last_grid
                    print("Success. "+str(undo)+" undo left")
                else:
                    print("No more undo available")
            else:
                print("There is no move to replace")
            grid_print(grid, number, theme)
            continue
        elif move == "H":
            if hint > 0:
                best_move, evaluation = grid_max(grid)
                hint -= 1
                print("The best move is "+best_move+". "+str(hint)+" hint left")
            else:
                print("No more hint available")
            continue
        new_grid  = grid_move(grid, COMMANDS[move])
        # Pas de déplacement dans la direction d donc on demande une autre direction
        if new_grid == grid:
            continue
        grid, last_grid = new_grid, grid
        # Ajout d'une nouvelle tuile
        grid_add_new_tile(grid)
        # Affichage de la grille
        grid_print(grid, number, theme)
    if grid_get_max_value(grid) >= 2048:
        print("You win !!")
    else:
        print("You lose...")
    # Ajout du score dans le classement
    add_leaderboard("leaderboard", pseudo, grid_score(grid), number)
    # Fin de la partie
    print("Your score is "+str(grid_score(grid)))
    print("Please restart the program to play a new game")

if __name__ == '__main__':
    play()
    exit(1)
