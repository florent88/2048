# Module game 2048

import random, pickle

VALUE = [2, 2, 2, 2, 2, 2, 2, 4, 4, 4] # 2 plus présent que les 4 (70 - 30)
DIRECTIONS = {"right": (0,1), "left": (0,-1), "up": (-1,0), "down": (1,0)}

def grid_init(n=4):
    """
    Initie une grille vierge

    valeur renvoyée: (list) la grille sous forme de liste
    """
    grid = []
    # Grille n x n
    for i in range(n):
        # 0 pour représenter les cases vides
        grid += [list(0 for j in range(n))]
    grid_add_new_tile(grid)
    return grid

def all_value(grid):
    """
    Retourne une liste contenant toutes les valeurs dans la grilles

    paramètre grid: (list) la grille sous forme de liste
    valeur renvoyée: (list) une liste contenant toutes les valeurs dans la grille

    Exemples:
    >>> all_value([[0,4,8,2], [0,0,0,0], [0,512,32,64], [1024,2048,512,0]])
    [0, 4, 8, 2, 0, 0, 0, 0, 0, 512, 32, 64, 1024, 2048, 512, 0]
    >>> all_value([[16,4,8,2], [2,4,2,128], [4,512,32,64], [1024,2048,512,2]])
    [16, 4, 8, 2, 2, 4, 2, 128, 4, 512, 32, 64, 1024, 2048, 512, 2]
    """
    res = []
    for line in grid:
        for value in line:
            res += [value]
    return res

def grid_print(grid,n=4):
    """
    Imprime la grille passée en paramètre
    
    paramètre grid: (list) la grille sous forme de liste
    """
    size_tile = len(str(grid_get_max_value(grid)))
    print('-'*((n+1) + size_tile * n))
    for line in grid:
        for value in line:
            print('|{:{align}{width}}'.format(value, align='^', width=str(size_tile)), end = '')
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
    return not 0 in all_value(grid)
            

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
    return max(all_value(grid))

def reverse(grid):
    reverse_grid = []
    for j in range(len(grid)):
        reverse_grid.append([grid[i][j] for i in range(len(grid))])
    return reverse_grid

def transpose(reverse_grid):
    grid = []
    for j in range(len(reverse_grid)):
        grid.append([reverse_grid[i][j] for i in range(len(reverse_grid))])
    return grid

def move_left(row):
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
        new = reverse(grid)
        for i in range(len(new)):
            new[i] = move_left(new[i])
        new = transpose(new)
    # Down
    elif x == 1:
        new = reverse(grid)
        for i in range(len(new)):
            row = new[i].copy()
            row.reverse()
            row = move_left(row)
            row.reverse()
            new[i] = row
        new = transpose(new)
    return new
     
def move_possible(grid):
    res = []
    # right, left, up, down
    for d in DIRECTIONS.keys():
        new = grid_move(grid, d)
        if new == grid:
            res += [False]
        else:
            res += [True]
    return res

def grid_add_new_tile(grid):
    """
    Ajoute une nouvelle tuile dans la grille passée en paramètre

    paramètre grid: (list) la grille sous forme de liste
    """
    coord = get_new_position(grid)
    x, y = coord[0], coord[1]
    grid[x][y] = random.choice(VALUE)

def get_new_position(grid):
    """
    Retourne un couple de coordonnée d'une tuile vide dans la grille passée en paramètre

    paramètre grid: (list) la grille sous forme de liste
    valeur renvoyée: (tuple) un couple de coordonnée d'une tuile vide
    """
    liste = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid_get_value(grid, (x, y)) == 0:
                liste += [(x, y)]
    return random.choice(liste)

def grid_get_value(grid, coord):
    """
    Retourne la valeur de la tuile possédant les coordonnées dans le couple

    paramètre grid: (list) la grille sous forme de liste
    paramètre coord: (tuple) un couple de coordonnée
    valeur renvoyée: (int) la valeur de la tuile possédant les coordonnées du couple, None sinon

    Exemples:
    >>> grid = [[0, 2, 4, 0], [2048, 512, 32, 0], [16, 32, 0, 4], [0, 0, 128, 254]]
    >>> grid_get_value(grid, (4, 4)) == None
    True
    >>> grid_get_value(grid, (1, 0))
    2048
    >>> grid_get_value(grid, (3, 2))
    128
    """
    x, y = coord[0], coord[1]
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
    >>> grid_get_next(grid, 0, 0, DIRECTIONS["up"]) == None
    True
    >>> grid_get_next(grid, 1, 1, DIRECTIONS["left"])
    2048
    >>> grid_get_next(grid, 3, 0, DIRECTIONS["down"]) == None
    True
    >>> grid_get_next(grid, 2, 1, DIRECTIONS["up"])
    512
    """
    coord_x, coord_y = d[0], d[1]
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
    >>> grid = [[0, 2, 0, 4], [32, 8, 0, 0], [0, 0, 8, 2], [64, 32, 0, 0]]
    >>> grid_score(grid)
    152
    >>> grid_2 = [[2, 0, 0, 4], [2048, 512, 0, 8], [64, 8, 16, 0], [8, 4, 2, 0]]
    >>> grid_score(grid_2)
    2676
    """
    res = 0
    for value in all_value(grid):
        res += value
    return res

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
    """
    with open(fname, 'rb') as file:
        liste = pickle.load(file)
    return liste

if __name__ == '__main__':
    import doctest
    doctest.testmod()
