import random, pickle

VALUE = [2, 2, 2, 2, 2, 2, 2, 4, 4, 4] # 2 plus présent que les 4 (70% - 30%)
DIRECTIONS = {"right": (0,1), "left": (0,-1), "up": (-1,0), "down": (1,0)}
# Themes disponibles (0 Default, 1 Chemistry, 2 Alphabet)
THEMES = {"0": {"name": "Default", 0: "", 2: "2", 4: "4", 8: "8", 16: "16", 32: "32", 64: "64", 128: "128", 256: "256", 512: "512", 1024: "1024", 2048: "2048", 4096: "4096", 8192: "8192"}, "1": {"name": "Chemistry", 0: "", 2: "H", 4: "He", 8: "Li", 16: "Be", 32: "B", 64: "C", 128: "N", 256: "O", 512: "F", 1024: "Ne", 2048: "Na", 4096: "Mg", 8192: "Al"}, "2": {"name": "Alphabet", 0: "", 2: "A", 4: "B", 8: "C", 16: "D", 32: "E", 64: "F", 128: "G", 256: "H", 512: "I", 1024: "J", 2048: "K", 4096: "L", 8192: "M"}}

def grid_init(n=4):
    """
    Initie une grille vierge

    paramètre n: (int) la taille de la grille nxn
    valeur renvoyée: (list) la grille sous forme de liste
    """
    grid = []
    # Grille de taille nxn
    for i in range(n):
        # 0 pour représenter les cases vides
        grid.append([0 for j in range(n)])
    # Ajout d'une tuile
    grid_add_new_tile(grid)
    return grid

def all_tiles(grid):
    """
    Retourne une liste contenant toutes les valeurs dans la grilles

    paramètre grid: (list) la grille sous forme de liste
    valeur renvoyée: (list) une liste contenant toutes les valeurs dans la grille

    Exemples:
    >>> all_tiles([[0,4,8,2], [0,0,0,0], [0,512,32,64], [1024,2048,512,0]])
    [0, 4, 8, 2, 0, 0, 0, 0, 0, 512, 32, 64, 1024, 2048, 512, 0]
    >>> all_tiles([[16,4,8,2], [2,4,2,128], [4,512,32,64], [1024,2048,512,2]])
    [16, 4, 8, 2, 2, 4, 2, 128, 4, 512, 32, 64, 1024, 2048, 512, 2]
    """
    tiles = []
    for row in grid:
        for tile in row:
            tiles.append(tile)
    return tiles

def long_value(grid, theme):
    """
    Récupère la taille de la plus grande tuile en fonction du theme

    paramètre grid: (list) la grille sous forme de liste
    paramètre theme: (dict) le thème séléctionné

    Exemples:
    >>> grid = [[2048, 16, 32, 0], [0, 4, 0, 2], [0, 0, 0, 32], [512, 1024, 0, 2]]
    >>> theme = {"name": "Default", 0: "", 2: "2", 4: "4", 8: "8", 16: "16", 32: "32", 64: "64", 128: "128", 256: "256", 512: "512", 1024: "1024", 2048: "2048", 4096: "4096", 8192: "8192"}
    >>> long_value(grid, theme)
    4
    >>> theme = {"name": "Default", 0: "", 2: "A", 4: "B", 8: "C", 16: "D", 32: "E", 64: "F", 128: "G", 256: "H", 512: "I", 1024: "J", 2048: "K", 4096: "L", 8192: "L"}
    >>> long_value(grid, theme)
    1
    """
    length = 0
    for tile in all_tiles(grid):
        if len(theme[tile]) > length:
            length = len(theme[tile])
    return length

def grid_print(grid, n=4, theme=THEMES["0"]):
    """
    Imprime la grille passée en paramètre
    
    paramètre grid: (list) la grille sous forme de liste
    paramètre n: (int) la taille de la grille
    paramètre theme: (dict) le thème a appliqué lors de l'affichage de la grille
    """
    size_tile = long_value(grid, theme)
    print('-'*((n+1) + size_tile * n))
    for row in grid:
        for tile in row:
            print('|{:{align}{width}}'.format(theme[tile], align='^', width=str(size_tile)), end = '')
        print('|')
        print('-'*((n+1) + size_tile * n))

def is_grid_over(grid):
    """
    Teste si la grille passée en paramètre est pleine ou non

    paramètre grid: (list) la grille sous forme de liste
    valeur renvoyée: (bool) True si la grille est pleine (valeurs différents de 0), False sinon

    Exemples:
    >>> is_grid_over([[0,4,8,2], [0,0,0,0], [0,512,32,64], [1024,2048,512,0]])
    False
    >>> is_grid_over([[16,4,8,2], [2,4,2,128], [4,512,32,64], [1024,2048,512,2]])
    True
    """
    return not 0 in all_tiles(grid)
            

def grid_get_max_value(grid):
    """
    Retourne la plus grande valeur dans la grille passée en paramètre

    paramètre grid: (list) la grille sous forme de liste
    valeur renvoyée: (int) la valeur maximale contenue dans la grille

    Exemples:
    >>> grid_get_max_value([[16,4,8,2], [2,4,2,128], [4,512,32,64], [1024,2048,512,2]])
    2048
    >>> grid_get_max_value([[16,4,8,2], [2,4,2,128], [4,512,32,64], [16,0,512,2]])
    512
    """
    return max(all_tiles(grid))

def transpose(grid):
    """
    Inverse l'horizontal et vertical de la grille, au lieu de lire de gauche à droite,  on lit de haut en bas

    paramètre grid: (list) la grille sous forme de liste

    Exemples:
    >>> transpose([[0, 2, 4, 8], [16, 32, 64, 0], [2, 2, 8, 128], [0, 4, 8, 2]])
    [[0, 16, 2, 0], [2, 32, 2, 4], [4, 64, 8, 8], [8, 0, 128, 2]]
    >>> transpose([[32, 64, 0, 4], [8, 4, 0, 2], [16, 32, 128, 0], [512, 128, 254, 4]])
    [[32, 8, 16, 512], [64, 4, 32, 128], [0, 0, 128, 254], [4, 2, 0, 4]]
    """
    new = []
    for j in range(len(grid)):
        new.append([grid[i][j] for i in range(len(grid))])
    return new

def move_left(row):
    """
    Effectue un déplacement à gauche d'une ligne

    paramètre row: (list) une liste de tuile

    Exemples:
    >>> move_left([0, 0, 0, 2])
    [2, 0, 0, 0]
    >>> move_left([0, 2, 0, 4])
    [2, 4, 0, 0]
    >>> move_left([2, 2, 0, 4])
    [4, 4, 0, 0]
    >>> move_left([2, 2, 2, 2])
    [4, 4, 0, 0]
    >>> move_left([4, 2, 0, 2])
    [4, 4, 0, 0]
    >>> move_left([2, 0, 0, 2])
    [4, 0, 0, 0]
    >>> move_left([2, 4, 2, 2])
    [2, 4, 4, 0]
    >>> move_left([4, 8, 16, 32])
    [4, 8, 16, 32]
    """
    new_row, k, prev = [0 for i in range(len(row))], 0, None
    for i in range(len(row)):
        # Tuile non vide
        if row[i] != 0:
            if prev is None:
                prev = row[i]
            else:
                # Tuile de même taille donc on les additionne
                if prev == row[i]:
                    new_row[k] = row[i]*2
                    k += 1
                    prev = None
                # Sinon on la décale
                else:
                    new_row[k] = prev
                    k += 1
                    prev = row[i]
    if prev is not None:
        new_row[k] = prev
    return new_row

def grid_move(grid, d):
    """
    Effectue le déplacement de la grille suivant la direction d

    paramètre grid: (list) la grille sous forme de liste
    paramètre d: (str) le déplacement à suivre

    Exemples:
    """
    new = grid.copy()
    d = DIRECTIONS[d]
    x, y = d[0], d[1]
    # Gauche
    if y == -1:
        for i in range(len(grid)):
            new[i] = move_left(grid[i])
    # Droite
    elif y == 1:
        for i in range(len(grid)):
            row = grid[i].copy()
            row.reverse()
            row = move_left(row)
            row.reverse()
            new[i] = row
    # Up
    elif x == -1:
        new = transpose(grid)
        for i in range(len(new)):
            new[i] = move_left(new[i])
        new = transpose(new)
    # Down
    elif x == 1:
        new = transpose(grid)
        for i in range(len(new)):
            row = new[i].copy()
            row.reverse()
            row = move_left(row)
            row.reverse()
            new[i] = row
        new = transpose(new)
    return new
     
def move_possible(grid):
    """
    Renvoie une liste de booléen si les déplacements dans chaques directions est possible

    paramètre grid: (list) la grille sous forme de liste

    Exemples:
    >>> move_possible([[2, 2, 2, 2], [4, 8, 8, 16], [0, 8, 0, 4], [4, 8, 16, 32]])
    [True, True, True, True]
    >>> move_possible([[2, 4, 8, 16], [16, 8, 4, 2], [2, 4, 8, 16], [16, 8, 4, 2]])
    [False, False, False, False]
    """
    moves = []
    # [RIGHT, LEFT, UP, DOWN]
    for d in DIRECTIONS.keys():
        new = grid_move(grid, d)
        if new == grid:
            moves.append(False)
        else:
            moves.append(True)
    return moves

def grid_add_new_tile(grid):
    """
    Ajoute une nouvelle tuile dans la grille passée en paramètre

    paramètre grid: (list) la grille sous forme de liste
    """
    coord = get_new_position(grid)
    x, y = coord
    grid[x][y] = random.choice(VALUE)

def empty_tiles(grid):
    """
    Renvoie une liste de coordonnée de tuile vide

    paramètre grid: (list) la grille sous forme de liste
    valeur renvoyée: (liste) une liste de tuple representant des coordonnées

    Exemples:
    >>> len(empty_tiles([[0, 16, 2, 4], [512, 128, 32, 0], [8, 16, 32, 4], [4, 0, 2, 2]]))
    3
    >>> len(empty_tiles([[16, 32, 64, 4], [64, 2, 512, 2], [8, 64, 16, 2], [4, 2, 8, 128]]))
    0
    """
    empty = []
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid_get_value(grid, (x, y)) == 0:
                empty.append((x, y))
    return empty

def get_new_position(grid):
    """
    Retourne un couple de coordonnée d'une tuile vide dans la grille passée en paramètre

    paramètre grid: (list) la grille sous forme de liste
    valeur renvoyée: (tuple) un couple de coordonnée d'une tuile vide

    Exemple:
    >>> grid = [[0, 16, 32, 0], [64, 0, 32, 2], [2, 2, 8, 4], [512, 8, 16, 0]]
    >>> x, y = get_new_position(grid)
    >>> grid_get_value(grid, (x, y))
    0
    """
    return random.choice(empty_tiles(grid))

def grid_get_value(grid, coord):
    """
    Retourne la valeur de la tuile possédant les coordonnées dans le couple

    paramètre grid: (list) la grille sous forme de liste
    paramètre coord: (tuple) un couple de coordonnée (x, y)
    valeur renvoyée: (int) la valeur de la tuile possédant les coordonnées du couple, None sinon

    Exemples:
    >>> grid = [[0, 2, 4, 0], [2048, 512, 32, 0], [16, 32, 0, 4], [0, 0, 128, 254]]
    >>> grid_get_value(grid, (4, 4)) is None
    True
    >>> grid_get_value(grid, (1, 0))
    2048
    >>> grid_get_value(grid, (3, 2))
    128
    """
    x, y = coord
    try:
        return grid[x][y]
    except:
        return None

def grid_get_next(grid, x, y, d):
    """
    Renvoie la valeur de la tuile à côté de coordonné (x, y) suivant la direction d

    paramètre grid: (list) la grille sous forme de liste
    paramètre x: (int) la coordonnée x de la tuile
    paramètre y: (int) la coordonnée y de la tuile
    paramètre d: (tuple) couple donnant la direction

    Exemples:
    >>> grid = [[0, 2, 4, 0], [2048, 512, 32, 0], [16, 32, 0, 4], [0, 0, 128, 254]]
    >>> grid_get_next(grid, 0, 0, DIRECTIONS["down"])
    2048
    >>> grid_get_next(grid, 0, 0, DIRECTIONS["up"]) is None
    True
    >>> grid_get_next(grid, 1, 1, DIRECTIONS["left"])
    2048
    >>> grid_get_next(grid, 3, 0, DIRECTIONS["down"]) is None
    True
    >>> grid_get_next(grid, 2, 1, DIRECTIONS["up"])
    512
    """
    coord_x, coord_y = d
    new_x, new_y = x + coord_x, y + coord_y
    # Coordonnée invalide
    if new_x < 0 or new_y < 0:
        return None
    return grid_get_value(grid, (new_x, new_y))

def grid_score(grid):
    """
    Calcule le score avec la grille passée en paramètre en additionnant toutes les tuiles

    paramètre grid: (list) la grille sous forme de liste
    valeur renvoyée: (int) la somme de toutes les tuiles

    Exemples:
    >>> grid_score([[0, 2, 0, 4], [32, 8, 0, 0], [0, 0, 8, 2], [64, 32, 0, 0]])
    152
    >>> grid_score([[2, 0, 0, 4], [2048, 512, 0, 8], [64, 8, 16, 0], [8, 4, 2, 0]])
    2676
    """
    score = 0
    for tile in all_tiles(grid):
        score += tile
    return score

def grid_save(grid, fname):
    """
    Sauvegarde la partie en cours

    paramètre grid: (list) la grille sous forme de liste
    paramètre fname: (str) le nom du fichier pour sauvegarder
    """
    with open(fname, 'wb') as file:
        pickle.dump(grid, file)

def grid_load(fname):
    """
    Charge une partie précédemment sauvegardé

    paramètre fname: (str) le nom du fichier contenant la sauvegarde
    valeur renvoyée: (list) la grille sauvegardée sous forme d'une liste
    """
    with open(fname, 'rb') as file:
        liste = pickle.load(file)
    return liste

def get_leaderboard(fname):
    """
    Charge le fichier contenant le classement et renvoie le classement sous forme d'une liste, si il n'existe pas il le crée et renvoie une liste vide

    paramètre fname: (str) le nom du fichier contenant le classement
    valeur renvoyée: (list) une liste de tuple (pseudo, score)
    """
    try:
        with open(fname, 'rb') as file:
            leaderboard = pickle.load(file)
    except FileNotFoundError:
        leaderboard = []
        save_leaderboard(fname, leaderboard)
    return leaderboard

def save_leaderboard(fname, leaderboard):
    """
    Sauvegarde la liste du classement dans un fichier

    paramètre fname: (str) le nom du fichier contenant le classement
    paramètre liste: (list) une liste de tuple (pseudo, score)
    """
    with open(fname, 'wb') as file:
        pickle.dump(leaderboard, file)

def add_leaderboard(fname, name, score, size):
    """
    Ajoute un nouveau joueur dans le classement

    paramètre fname: (str) le nom du fichier contenant le classement
    paramètre name: (str) le pseudo du joueur
    paramètre score: (int) le score de la partie
    paramètre size: (int) la taille de la grille jouée
    """
    leaderboard = get_leaderboard(fname)
    if len(leaderboard) >= 10: 
        i = 0
        while i < len(leaderboard):
            if leaderboard[i][0] <= score:
                leaderboard[i] = (score, name, size)
                break
    else:
        leaderboard.append((score, name, size))
        leaderboard.sort(reverse=True)
    save_leaderboard(fname, leaderboard)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
