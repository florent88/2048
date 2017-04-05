# Module graphique 2048

from tkinter import *
from tkinter.messagebox import *
from game_2048 import *

fenetre = None
grid = None
gr_grid = []
finish = False
lose = False
n = 4

TILES_BG_COLOR = {2: "#eee4da", 4: "#ede0c8", 8: "#f1b078", \
                  16: "#eb8c52", 32: "#f67c5f", 64: "#f65e3b", \
                  128: "#edcf72", 256: "#edcc61", 512: "#edc850", \
                  1024: "#edc53f", 2048: "#edc22e", 4096: "#5eda92", \
                  8192: "#24ba63"}

TILES_FG_COLOR = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2", \
                  32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", \
                  256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2", \
                  2048: "#f9f6f2", 4096: "#f9f6f2", 8192: "#f9f6f2"}

TILE_EMPTY_BG = "#9e948a"
TILES_FONT = {"Verdana", 40, "bold"}

GAME_SIZE = 600
GAME_BG = "#92877d" 
TILES_SIZE = GAME_SIZE // n

  
commands = {"Up": "up", "Left": "left", "Right": "right", "Down": "down" }

def new_game():
    """
    Créer une nouvelle partie
    """
    global grid, lose, finish, n
    lose, finish = False, False
    # Nouvelle partie
    showinfo("New game", "A new game start")
    grid = grid_init(n)
    grid_display(grid)

def load_game():
    """
    Charge une partie précédemment sauvegardée
    """
    global grid, lose, finish
    try:
        grid = grid_load("save")
        lose, finish = False, False
        showinfo("Load Game", "Your game was successfully load.")
    except FileNotFoundError:
        showinfo("Error", "There is no gamed save.")
    grid_display(grid)

def save_game():
    """
    Sauvegarde la partie en cours et ferme le jeu
    """
    global grid
    grid_save(grid, "save")
    showinfo("Save game", "Your game was successfully save.")
    fenetre.quit()

def callback():
    """
    Demande une dernière vérification avant de quitter le jeu
    """
    if askyesno("Quit", "Are you sure ?"):
        fenetre.quit()

def score():
    """
    Affiche le score de la partie en cours
    """
    global grid
    showinfo("Score", "Your score is "+str(grid_score(grid)))
    
def about():
    """
    Affiche les informations du jeu
    """
    showinfo("About", "Developped by...")

def main():
    """
    launch the graphical game
    
    UC : none
    """
    global fenetre, gr_grid, grid, n
    # Initialisation de la fenetre
    fenetre = Tk()
    fenetre.title('2048')
    fenetre.bind("<Key>", key_pressed)
    fenetre.resizable(False, False)
    fenetre.grid()
    # Menubar
    menubar = Menu(fenetre)
    
    partie = Menu(menubar, tearoff = 0)
    partie.add_command(label = "New", command = new_game)
    partie.add_command(label = "Load", command = load_game)
    partie.add_command(label = "Save", command = save_game)
    partie.add_separator()
    partie.add_command(label = "Quit", command = callback)
    menubar.add_cascade(label = "Game", menu = partie)

    aide = Menu(menubar, tearoff = 0)
    aide.add_command(label = "About", command = about)
    menubar.add_cascade(label = "Help", menu = aide)

    menubar.add_command(label = "Score", command = score)
    
    fenetre.config(menu = menubar)
    # Génération de la grille
    background = Frame(fenetre, bg=GAME_BG)
    background.grid()
    gr_grid = []
    for i in range(n):
        gr_line = []
        for j in range(n):
            cell = Frame(background, bg=TILE_EMPTY_BG, width=TILES_SIZE, height=TILES_SIZE)
            cell.grid(row=i, column=j, padx=1, pady=1)
            t = Label(master = cell, text = "", bg = TILE_EMPTY_BG,
                      justify = CENTER, font = TILES_FONT,
                      width=8, height=4)
            t.grid()
            gr_line.append(t)
        gr_grid.append(gr_line)
    # Début du jeu
    new_game()
    # Boucle
    fenetre.mainloop()

def grid_display(grid):
    """
    graphical grid display
    
    UC : none
    """
    global gr_grid, fenetre, n
    for i in range(n):
        for j in range(n):
            number = grid_get_value(grid, (i, j))
            if number == 0:
                gr_grid[i][j].configure(text="", bg=TILE_EMPTY_BG)
            else:
                gr_grid[i][j].configure(text=str(number), \
                                        bg=TILES_BG_COLOR[number], \
                                        fg=TILES_FG_COLOR[number])
    fenetre.update_idletasks()

def key_pressed(event):
    """
    key press event handler
    
    UC : none
    """
    global fenetre, grid, finish, lose
    key = event.keysym
    # Inutile dès que le jeu est terminé
    if not lose:
        if key in commands:
            new_grid = grid_move(grid, commands[key])
            # Tant qu'un mouvement est possible on continuer à jouer
            if grid != new_grid and (not is_grid_over(grid) or True in move_possible(grid)):
                grid = new_grid
                grid_add_new_tile(grid)
            # Refresh de l'interface
            grid_display(grid)
            # Affichage du message de victoire
            if grid_get_max_value(grid) == 2048 and not finish:
                showinfo("2048", "You won !")
                finish = True
            # Affichage du message de fin
            if is_grid_over(grid) and not True in move_possible(grid):
                showinfo("2048", "You lose !")
                lose = True
        
if __name__ == '__main__':
    import sys
    main()
    exit(0)
