# Module graphique

from tkinter import *
from tkinter.messagebox import *
from game_2048 import *

fenetre = None
grid = None
gr_grid = []

TILES_BG_COLOR = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 
                  16:"#f59563", 32:"#f67c5f", 64:"#f65e3b",
                  128:"#edcf72", 256:"#edcc61", 512:"#edc850", 
                  1024:"#edc53f", 2048:"#edc22e" }

TILES_FG_COLOR = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                   32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                   512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }

TILE_EMPTY_BG = "#9e948a"
TILES_FONT = {"Verdana", 40, "bold"}

GAME_SIZE = 600
GAME_BG = "#92877d" 
TILES_SIZE = GAME_SIZE // 4

  
commands = { "Up" : "up", "Left" : "left", "Right" : "right", "Down" : "down" }

def new_game():
    showinfo("Error", "Coming soon")

def load_game():
    showinfo("Error", "Coming soon")

def callback():
    if askyesno("Quitter la partie", "Êtes-vous sûr de vouloir faire ça?"):
        fenetre.destroy()

def about():
    showinfo("A propos", "Blabla")

def main():
    """
    launch the graphical game
    
    UC : none
    """
    global fenetre, gr_grid,grid
    
    fenetre = Tk()
    fenetre.title('2048')
    # Menu
    menubar = Menu(fenetre)
    
    partie = Menu(menubar, tearoff = 0)
    partie.add_command(label = "Nouvelle", command = new_game)
    partie.add_command(label = "Charger", command = load_game)
    partie.add_separator()
    partie.add_command(label = "Quitter", command = callback)
    menubar.add_cascade(label = "Partie", menu = partie)

    aide = Menu(menubar, tearoff = 0)
    aide.add_command(label = "A propos", command = about)
    menubar.add_cascade(label = "Aide", menu = aide)
    
    fenetre.config(menu = menubar)
    # Grille
    fenetre.grid()
    fenetre.bind("<Key>", key_pressed)
    background = Frame(fenetre, bg = GAME_BG,
                       width=GAME_SIZE, height=GAME_SIZE)
    background.grid()
    gr_grid = []
    for i in range(4):
        gr_line = []
        for j in range(4):
            cell = Frame(background, bg = TILE_EMPTY_BG,
                         width = TILES_SIZE, height = TILES_SIZE)
            cell.grid(row=i, column=j,padx=1, pady=1)
            t = Label(master = cell, text = "", bg = TILE_EMPTY_BG,
                      justify = CENTER, font = TILES_FONT,
                      width=4, height=2)
            t.grid()
            gr_line.append(t)
        gr_grid.append(gr_line)
    grid = grid_init()
    grid_display(grid)
    fenetre.mainloop()

def grid_display(grid):
    """
    graphical grid display
    
    UC : none
    """
    global gr_grid, fenetre
    for i in range(4):
        for j in range(4):
            number= grid_get_value(grid, (i, j))
            if number == 0:
                gr_grid[i][j].configure(text="", bg=TILE_EMPTY_BG)
            else:
                gr_grid[i][j].configure(text=str(number), 
                                        bg=TILES_BG_COLOR[number],
                                        fg=TILES_FG_COLOR[number])
    fenetre.update_idletasks()

def key_pressed(event):
    """
    key press event handler
    
    UC : none
    """
    global fenetre, grid
    
    key = event.keysym
    if key in commands:
        grid_temp, has_moved = grid_move(grid, commands[key])
        if has_moved:
            grid = grid_temp
            grid_add_new_tile(grid)
        if is_grid_over(grid):
            print("You loose !!!")
        if grid_get_max_value(grid) == 2048:
            print("You win !!!")
        grid_display(grid)
        
if __name__ == '__main__':
    import sys

    main()
    exit(0)
