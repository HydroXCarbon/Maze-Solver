import sys
from graphic import Window, CustomButton
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
    seed = 1  # if seed = 0 -> fix seed
    random_index = True
    running = True 
    maze = None
    win = Window(screen_x, screen_y)
    
    button = CustomButton(win)
    

    while running:
        maze = Maze(random_index, margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed)
        response = button.wait_for_response()

        if response == "DFS":
            maze.solve_dfs()
        elif response == "BFS":
            maze.solve_bfs()
        elif response == "NEXT":
            pass
        elif response == "EXIT":
            running = False
            win.close()
        win.clear()
    
    win.wait_for_close()
    sys.exit()  # Exit the program

main()
