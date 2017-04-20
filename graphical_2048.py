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
theme_id = "0"
pseudo = None
undo = 2
last_grid = None

TILES_BG_COLOR = {0: "#9e948a", 2: "#eee4da", 4: "#ede0c8", 8: "#f1b078", \
                  16: "#eb8c52", 32: "#f67c5f", 64: "#f65e3b", \
                  128: "#edcf72", 256: "#edcc61", 512: "#edc850", \
                  1024: "#edc53f", 2048: "#edc22e", 4096: "#5eda92", \
                  8192: "#24ba63"}

TILES_FG_COLOR = {0: "#776e65", 2: "#776e65", 4: "#776e65", 8: "#f9f6f2", \
                  16: "#f9f6f2", 32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", \
                  256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2", \
                  2048: "#f9f6f2", 4096: "#f9f6f2", 8192: "#f9f6f2"}

TILES_FONT = {"Verdana", 40, "bold"}

GAME_SIZE = 600
GAME_BG = "#92877d" 
TILES_SIZE = GAME_SIZE // n

COMMANDS = {"Up": "up", "Left": "left", "Right": "right", "Down": "down"}

def get_center_position(tk, width, height):
    """
    Retourne la position du milieu de l'écran en fonction de la taille de ma fenetre et de ses dimensions
    """
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    x = screen_width//2 - width//2
    y = screen_height//2 - height//2
    return "{}x{}+{}+{}".format(width, height, x, y)

def save_game():
    """
    Sauvegarde la partie en cours
    """
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

def commands():
    """
    Affiche les commandes du jeu
    """
    showinfo("2048", "Use directional arrows to move the grid and obtain the 2048 tile")
    
def play():
    """
    Lancement de la partie
    """
    global n, grid, gr_grid, theme_id, pseudo

    def leaderboard():
        # Récupération du classement
        liste = get_leaderboard("leaderboard")
        # Création du popup
        win = Toplevel(game)
        win.title("Leaderboard")
        win.resizable(False, False)
        win.geometry(get_center_position(win, 250, 35 + 17*len(liste)))
        # Affichage du classement
        for score, name, size in liste:
            Label(win, text=name+" - Score "+str(score)+" - Grille "+str(size)+"x"+str(size)).pack()
        button = Button(win, text="Fermer", command=win.destroy).pack(side=BOTTOM, pady=5)
        # Boucle
        win.mainloop()
    
    def back():
        global lose, finish, undo, last_grid
        lose, finish, undo, last_grid = False, False, 2, None
        # Destruction de la fenetre de la partie
        game.destroy()
        # Agrandissement du menu principal
        root.deiconify()

    def grid_display(grid):
        global n, gr_grid, theme_id
        for i in range(n):
            for j in range(n):
                number = grid_get_value(grid, (i, j))
                gr_grid[i][j].configure(text=THEMES[theme_id][number], \
                                        bg=TILES_BG_COLOR[number], \
                                        fg=TILES_FG_COLOR[number])
        game.update_idletasks()

    def key_pressed(event):
        global grid, finish, lose, last_grid
        key = event.keysym
        # Inutile dès que l'utilisateur a perdu
        if not lose:
            if key in COMMANDS:
                new_grid = grid_move(grid, COMMANDS[key])
                # Tant qu'un mouvement est possible on continuer à jouer
                if grid != new_grid and (not is_grid_over(grid) or True in move_possible(grid)):
                    grid, last_grid = new_grid, grid
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
                    # Ajout du score dans le classement
                    add_leaderboard("leaderboard", pseudo, grid_score(grid), n)
                    lose = True

    def last_move():
        global undo, grid, last_grid
        if not last_grid is None and last_grid != grid:
            if undo > 0:
                undo -= 1
                # Remplacement et refresh de l'affichage
                grid = last_grid
                grid_display(grid)
                showinfo("2048", "Success.\n"+str(undo)+" undo left.")
            else:
                showerror("2048", "You spent all your undo")
        else:
            showerror("2048", "There is no move to replace")

    if len(pseudo_entry.get()) > 0:
        # Reduction du menu principal
        root.withdraw()
        # Récupération du pseudo
        pseudo = pseudo_entry.get()
        # Récupération du thème
        try:
            theme_id = str(list_theme.curselection()[0])
        # Aucune séléction donc thème par défault
        except IndexError:
            theme_id = "0"
        # Gestion de la partie sauvegardée
        if isfile("save"):
            if askyesno("2048", "A save is detected, do you want to load her ?"):
                # Récupération de la sauvegarde
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
        # Création de la fenetre pour le jeu
        game = Toplevel(root)
        game.title("2048")
        game.bind("<Key>", key_pressed)
        game.resizable(False, False)
        game.grid()
        # Ajout du menu
        menubar = Menu(game)
    
        partie = Menu(menubar, tearoff=0)
        partie.add_command(label="New", command=back)
        partie.add_command(label="Save", command=save_game)
        partie.add_separator()
        partie.add_command(label="Quit", command=quit_game)
        menubar.add_cascade(label="Game", menu=partie)

        menubar.add_command(label="Undo", command=last_move)

        menubar.add_command(label="Score", command=score)

        menubar.add_command(label="Leaderboard", command=leaderboard)

        aide = Menu(menubar, tearoff=0)
        aide.add_command(label="About", command=about)
        aide.add_command(label="Commands", command=commands)
        menubar.add_cascade(label="Help", menu=aide)
    
        game.config(menu=menubar)
        # Génération de la grille de fond
        background = Frame(game, bg=GAME_BG)
        background.grid()
        gr_grid = []
        for i in range(n):
            gr_line = []
            for j in range(n):
                cell = Frame(background, bg=TILES_BG_COLOR[0], width=TILES_SIZE, height=TILES_SIZE)
                cell.grid(row=i, column=j, padx=1, pady=1)
                t = Label(master=cell, text="", bg=TILES_BG_COLOR[0], \
                          justify=CENTER, font=TILES_FONT, \
                          width=8, height=4)
                t.grid()
                gr_line.append(t)
            gr_grid.append(gr_line)
        # Affichage de la grille
        grid_display(grid)
        # Centrage de la fenetre
        game.geometry(get_center_position(game, game.winfo_width(), game.winfo_height()))
        # Boucle de la partie
        game.mainloop()
    else:
        showerror("2048", "Please enter a pseudo before play")
        
# Création du menu
root = Tk()
root.title("2048")
root.geometry(get_center_position(root, 250, 215))
root.resizable(False, False)
# Initialisation des widgets
label_pseudo = Label(root, text="Choose your pseudo")
pseudo_entry = Entry(root)
label = Label(root, text="Choose grid size")
spin = Spinbox(root, from_=4, to=8)
label_theme = Label(root, text="Choose a theme")
list_theme = Listbox(root, selectmode="single")
list_theme.config(height=4)
button = Button(root, text="Play", command=play)
button_quit = Button(root, text="Quit", command=quit_game)
# Récupération des thèmes dans le module game
for key in THEMES.keys():
    list_theme.insert(key, THEMES[key]["name"])
# Affichage des widgets
label_pseudo.pack(pady=5)
pseudo_entry.pack()
label.pack()
spin.pack()
label_theme.pack()
list_theme.pack()
button.pack(side=RIGHT, padx=5, pady=5)
button_quit.pack(side=LEFT, padx=5, pady=5)
# Boucle
root.mainloop()
