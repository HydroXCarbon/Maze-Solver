from graphic import Window
from maze import Maze
import random

def main():
    margin = 50
    num_rows = 40
    num_cols = 40
    screen_x = 1100
    screen_y = 800
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    seed = 0
    random_index = True

    win = Window(screen_x, screen_y)

    for i in range(10):
        maze = Maze(random_index, margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed)
        maze.solve()
        win.clear()
        
    win.wait_for_close()


main()
