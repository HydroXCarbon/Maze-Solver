from cell import Cell
import time
import random

class Maze:
    
    def __init__(
        self,
        random_index,
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
        self._random = random_index
        if seed:
            random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r()
        self._check_random()
        self._reset_cells_visited()
    
    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        self._check_random()

    def _check_random(self):
        if not self._random:
            for i in range(self._num_cols):
                for j in range(self._num_rows):
                    self._draw_cell(i, j)
        else:
            indices = [(i, j) for i in range(self._num_cols) for j in range(self._num_rows)]
            random.shuffle(indices)
            for i, j in indices:
                self._draw_cell(i, j)
       
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        cell = self._cells[i][j]  
        cell.draw(x1, y1, x2, y2)

        self._animate(True)

    def _animate(self, speed=False):
        if self._win is None:
            return
        self._win.redraw()
        if not speed:
            time.sleep(0.005)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False 
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False 
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols-1, self._num_rows-1)
    
    def _break_walls_r(self, i=0, j=0):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []
            possible_direction_indexes = 0

            # check all possible directions
            # check top
            if j > 0 and not self._cells[i][j-1].visited:
                next_index_list.append((i, j-1))
                possible_direction_indexes += 1

            # check right
            if i < self._num_cols-1 and not self._cells[i+1][j].visited:
                next_index_list.append((i+1, j))
                possible_direction_indexes += 1

            # check bottom
            if j < self._num_rows-1 and not self._cells[i][j+1].visited:
                next_index_list.append((i, j+1))
                possible_direction_indexes += 1

            # check left
            if i > 0 and not self._cells[i-1][j].visited:
                next_index_list.append((i-1, j))
                possible_direction_indexes += 1

            if possible_direction_indexes == 0:
                return

            # random direction
            direction_index = random.randrange(possible_direction_indexes)
            next_index = next_index_list[direction_index]

            # knock wall down

            # knock top
            if next_index[1] < j:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False

            # knock right
            if next_index[0] > i:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False

            # knock bottom
            if next_index[1] > j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False

            # knock left
            if next_index[0] < i:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False

            self._break_walls_r(next_index[0], next_index[1])
            
    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve_dfs(self):
        return self._solve_r_1(0, 0)

    def _solve_r_1(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        # check end
        if i == self._num_cols-1 and j == self._num_rows-1:
            return True
        
        # check all direction

        # check bottom
        if j < self._num_rows-1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].visited:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r_1(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
                        
        # check right
        if i < self._num_cols-1 and not self._cells[i][j].has_right_wall and not self._cells[i+1][j].visited:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r_1(i+1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)

        # check top
        if j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j-1].visited:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r_1(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)

        # check left
        if i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i-1][j].visited:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r_1(i-1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)

        return False

    def solve_bfs(self):
        return self._solve_r_2(0, 0) 
    
    def _solve_r_2(self, i, j):
        back_tracking_dict = {}
        to_visit = []
        to_visit.append([i, j, 0])
        while to_visit:
            neighbours = []
            s = to_visit.pop(0)
            i = s[0]
            j = s[1]
            direction = s[2]
            self._cells[i][j].visited = True

            # knock walls
            if direction is not 0:
                
                # knock top
                if direction == 1:
                    self._cells[i][j+1].draw_move(self._cells[i][j], True)
                # knock right
                elif direction == 2:
                    self._cells[i-1][j].draw_move(self._cells[i][j], True)
                # knock bottom
                elif direction == 3:
                    self._cells[i][j-1].draw_move(self._cells[i][j], True)
                # knock left
                elif direction == 4:
                    self._cells[i+1][j].draw_move(self._cells[i][j], True)

                self._animate()

            # check end
            if i == self._num_cols-1 and j == self._num_rows-1:
                self.back_tracking_r_2(back_tracking_dict)
                return True
            
            # check all direction

            # check bottom
            if j < self._num_rows-1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].visited:
                neighbours.append([i, j+1, 3])
                back_tracking_dict[(i, j+1)] = (i, j)

            # check right
            if i < self._num_cols-1 and not self._cells[i][j].has_right_wall and not self._cells[i+1][j].visited:
                neighbours.append([i+1, j, 2])
                back_tracking_dict[(i+1, j)] = (i, j)

            # check top
            if j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j-1].visited:
                neighbours.append([i, j-1, 1])
                back_tracking_dict[(i, j-1)] = (i, j)

            # check left
            if i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i-1][j].visited:
                neighbours.append([i-1, j, 4])
                back_tracking_dict[(i-1, j)] = (i, j)

            random.shuffle(neighbours)
            for neighbour in neighbours:
                to_visit.append(neighbour)
        
        return False
    
    def back_tracking_r_2(self, back_tracking_dict):
        
        start = (self._num_cols-1, self._num_rows-1)
        end = (0, 0)
        current = start
        while current != end:
            temp = current
            current = back_tracking_dict[(current[0],current[1])]
            self._cells[temp[0]][temp[1]].draw_move(self._cells[current[0]][current[1]], False)
            self._animate()

        return True