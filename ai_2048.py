from game_2048 import *

def grid_evaluate(grid):
    """
    Evalue la grille passée en paramètre en fonction de la plus grande tuile, du nombre de case vide et de la régularité de celle-ci

    paramètre grid: (list) la grille sous forme de liste
    valeur renvoyée: (int) le score de la grille
    """
    regularity, score, max_tile, number_empty_tiles = 0, grid_score(grid), grid_get_max_value(grid), len(empty_tiles(grid))
    # Evaluation de la régularité de la grille
    n = len(grid)
    # Vertical
    for x in range(len(grid)):
        y = 0
    # Horizontal
    for y in range(len(grid)):
        x = 0
    return regularity + score + max_tile + 32 * number_empty_tiles

def grid_max(grid):
    """
    Retourne le meilleur mouvement à faire

    paramètre grid: (list) la grille sous forme de liste
    valeur renvoyée: (tuple) un couple (direction, point) indiquant le meilleur mouvement
    """
    best_score = 0
    best_move = None
    for move in DIRECTIONS.keys():
        new_grid = grid_move(grid, move)
        if new_grid == grid:
            continue
        else:
            new_score = grid_evaluate(new_grid)
        if new_score > best_score:
            best_score, best_move = new_score, move
    return (best_move, best_score)
