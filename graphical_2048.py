from tkinter import *
from tkinter.messagebox import *
from game_2048 import *
from os.path import *
from os import remove

# Déclaration des constantes
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

def get_center_position(tk, width, height):
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    x = screen_width//2 - width//2
    y = screen_height//2 - height//2
    return "{}x{}+{}+{}".format(width, height, x, y)

# Création du menu
root = Tk()
root.title("2048")
root.geometry(get_center_position(root, 250, 100))
root.resizable(False, False)

def save_game():
    global grid
    grid_save(grid, "save")
    showinfo("2048", "Your game was successfully save.")
    root.destroy()

def quit_game():
    """
    Demande une dernière vérification avant de quitter le jeu
    """
    if askyesno("2048", "Are you sure ?"):
        root.destroy()

def score():
    """
    Affiche le score de la partie en cours
    """
    global grid
    showinfo("2048", "Your score is "+str(grid_score(grid)))
    
def about():
    """
    Affiche les informations du jeu
    """
    showinfo("2048", "Developped by...")
    
def play():
    global n, grid, gr_grid
    
    def back():
        # Destruction de la partie courante
        game.destroy()
        # Agrandissement du menu principal
        root.deiconify()

    def grid_display(grid):
        global n, gr_grid
        for i in range(n):
            for j in range(n):
                number = grid_get_value(grid, (i, j))
                if number == 0:
                    gr_grid[i][j].configure(text="", bg=TILE_EMPTY_BG)
                else:
                    gr_grid[i][j].configure(text=str(number), \
                                            bg=TILES_BG_COLOR[number], \
                                            fg=TILES_FG_COLOR[number])
        game.update_idletasks()

    def key_pressed(event):
        global grid, finish, lose
        key = event.keysym
        # Inutile dès que l'utilisateur a perdu
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

    # Reduction du menu principal
    root.withdraw()
    # Gestion du fichier sauvegarde
    if isfile("save"):
        if askyesno("2048", "A save is detected, do you want to load her ?"):
            grid = grid_load("save")
            n = len(grid)
            # Suppression du fichier sauvegarde
            remove("save")
        else:
            n = int(spin.get())
            grid = grid_init(n)
    else:
        n = int(spin.get())
        grid = grid_init(n)
    # Création de la partie
    game = Toplevel(root)
    game.title("2048")
    game.bind("<Key>", key_pressed)
    game.resizable(False, False)
    game.grid()
    # Ajout du menu
    menubar = Menu(game)
    
    partie = Menu(menubar, tearoff = 0)
    partie.add_command(label = "New", command = back)
    partie.add_command(label = "Save", command = save_game)
    partie.add_separator()
    partie.add_command(label = "Quit", command = quit_game)
    menubar.add_cascade(label = "Game", menu = partie)

    menubar.add_command(label = "Score", command = score)

    aide = Menu(menubar, tearoff = 0)
    aide.add_command(label = "About", command = about)
    menubar.add_cascade(label = "Help", menu = aide)
    
    game.config(menu = menubar)
    # Génération de la grille de fond
    background = Frame(game, bg=GAME_BG)
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
    # Affichage de la grille
    grid_display(grid)
    # Centrage de la fenetre
    game.geometry(get_center_position(game, game.winfo_width(), game.winfo_height()))
    # Boucle secondaire
    game.mainloop()

# Initialisation des widgets
label = Label(root, text="Choose grid size")
spin = Spinbox(root, from_=3, to=7)
button = Button(root, text="Play", command=play)
button_quit = Button(root, text="Quit", command=quit_game)
# Affichage des widgets
label.pack(pady=5)
spin.pack()
button.pack(side=RIGHT, padx=5, pady=5)
button_quit.pack(side=LEFT, padx=5, pady=5)
# Boucle principale
root.mainloop()
