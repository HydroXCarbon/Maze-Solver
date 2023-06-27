from cell import Cell
import time
import random

class Maze:
    
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed
        
        self._create_cells()
    
    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)

        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False 
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False 
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols-1, self._num_rows-1)
    
    def _break_walls_r(self, i=0, j=0):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            posible_direction_indexes = 0

            #check all posible direction
            print("test1")
            #check top
            if j > 0 and not self._cells[i][j-1].visited:
                next_index_list.append((i, j-1))
                posible_direction_indexes += 1
            
            #check right
            if i+1 < self._num_cols-1 and not self._cells[i+1][j].visited:
                next_index_list.append((i+1, j))
                posible_direction_indexes += 1

            #check bottom
            if j+1 < self._num_rows-1 and not self._cells[i][j+1].visited:
                next_index_list.append((i, j+1))
                posible_direction_indexes += 1

            #check left
            if i > 0 and not self._cells[i-1][j].visited:
                next_index_list.append((i-1, j))
                posible_direction_indexes += 1

            if posible_direction_indexes == 0:
                return
            print("test2")
            #random direction 
            direction_index = random.randrange(posible_direction_indexes) 
            next_index = next_index_list[direction_index]

            #knock wall down

            #knock top
            if next_index[1] < j:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False

            #knock right
            if next_index[0] > i:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False

            #knock bottom
            if next_index[1] > j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False

            #knock left
            if next_index[0] < i:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_rihgt_wall = False
            print("test3")
            self._win.redraw()
            self._break_walls_r(next_index[0], next_index[1])
            




            
