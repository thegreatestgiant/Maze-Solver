from cell import Cell
from graphics import Point
import time, random


class Maze:

  def __init__(
    self,
    x1,
    y1,
    num_rows,
    num_cols,
    cell_size_x,
    cell_size_y,
    win=None,
  ):
    self._cells = []
    self._x1 = x1
    self._y1 = y1
    self._num_rows = num_rows
    self._num_cols = num_cols
    self._cell_size_x = cell_size_x
    self._cell_size_y = cell_size_y
    self._win = win
    self._create_cells()
    self._break_entrance_and_exit()
    self._break_walls_r(0, 0)
    self._reset_cells_visited()

  def _create_cells(self):
    for i in range(self._num_cols):
      col_cells = []
      for j in range(self._num_rows):
        col_cells.append(Cell(self._win))
      self._cells.append(col_cells)
    for i in range(self._num_cols):
      for j in range(self._num_rows):
        self._draw_cell(i, j)

  def _break_entrance_and_exit(self):
    self._cells[0][0].has_top_wall = False
    self._draw_cell(0, 0)
    lcol = self._num_cols - 1
    lrow = self._num_rows - 1
    self._cells[lcol][lrow].has_bottom_wall = False
    self._draw_cell(lcol, lrow)

  def _draw_cell(self, i, j):
    if self._win == None:
      return
    top_left = Point(self._x1 + i * self._cell_size_x,
                     self._y1 + j * self._cell_size_y)
    bottom_right = Point(self._x1 + (i + 1) * self._cell_size_x,
                         self._y1 + (j + 1) * self._cell_size_y)
    self._cells[i][j].draw(top_left, bottom_right)
    self._animate()

  def _animate(self):
    if self._win == None:
      return

    self._win.redraw()
    time.sleep(.05)

  def _break_walls_r(self, i, j):
    # Set the current cell as visited
    self._cells[i][j]._visited = True
    max_i = self._num_cols - 1
    max_j = self._num_rows - 1
    while True:
      # Create a list with all possible labels
      to_visit = [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]
      # Remove the labels that are out of bounds
      if i == 0:
        to_visit.remove([i - 1, j])
      if i == max_i:
        to_visit.remove([i + 1, j])
      if j == 0:
        to_visit.remove([i, j - 1])
      if j == max_j:
        to_visit.remove([i, j + 1])
      # If there are no more cells to visit
      # enact changes and break
      if len(to_visit) == 0:
        self._draw_cell(i, j)
        return
      # Pick a random cell
      k, l = random.choice(to_visit)
      # Make sure that cell has not been visited
      # If it has than pick a new one or break
      while self._cells[k][l]._visited:
        if [k, l] in to_visit:
          to_visit.remove([k, l])
        if len(to_visit) == 0:
          self._draw_cell(i, j)
          return
        k, l = random.choice(to_visit)

      # Break the wall between the current cell and the chosen cell
      # right
      if k == i + 1:
        self._cells[i][j].has_right_wall = False
        self._cells[k][l].has_left_wall = False
      # left
      if k == i - 1:
        self._cells[i][j].has_left_wall = False
        self._cells[k][l].has_right_wall = False
      # down
      if l == j + 1:
        self._cells[i][j].has_bottom_wall = False
        self._cells[k][l].has_top_wall = False
      # up
      if l == j - 1:
        self._cells[i][j].has_top_wall = False
        self._cells[k][l].has_bottom_wall = False
      # Send the virus to the next cell
      self._break_walls_r(k, l)

  def _reset_cells_visited(self):
    for i in range(self._num_cols):
      for j in range(self._num_rows):
        self._cells[i][j]._visited = False

  def solve(self):
    return self._solve_r(0, 0)

  def _solve_r(self, i, j):
    self._animate()
    cell = self._cells[i][j]
    cell._visited = True
    if i == self._num_cols - 1 and j == self._num_rows - 1:
      return True
    directions = []
    # right
    if not cell.has_right_wall:
      directions.append([i + 1, j])
    # left
    if not cell.has_left_wall:
      directions.append([i - 1, j])
    # up
    if not cell.has_top_wall and not i == 0:
      directions.append([i, j - 1])
    # down
    if not cell.has_bottom_wall and not j == self._num_rows - 1:
      directions.append([i, j + 1])
    print(f"Directions for ({i}, {j}): {directions}")
    for k, l in directions:
      if self._cells[k][l]._visited:
        continue
      cell.draw_move(self._cells[k][l])
      if self._solve_r(k, l):
        return True
      else:
        cell.draw_move(self._cells[k][l], True)
    return False