from game_2048 import *

def grid_evaluate(grid):
    score = grid_score(grid)
    max_value = grid_get_max_value(grid)
    empty_tiles = number_empty_tiles(grid)

    return score + max_value + empty_tiles

def grid_max(grid):
    score=0
    best=None
    for move in MOVE:
        new_grid=grid.copy()
        new_grid=grid_move(grid,MOVE[move])
        new_score=grid_evaluate(new_grid)
        if new_score>score:
            score = new_score
            best=move
    return (best,score)
