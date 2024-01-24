from graphics import Line, Point


class Cell:

  def __init__(self, win=None, left=True, right=True, top=True, bottom=True):
    self._win = win
    self.has_left_wall = left
    self.has_right_wall = right
    self.has_top_wall = top
    self.has_bottom_wall = bottom
    self._visited = False

  def draw(self, top_left, bottom_right):
    if self._win == None:
      return
    self.x1 = top_left.x
    self.y1 = top_left.y
    self.x2 = bottom_right.x
    self.y2 = bottom_right.y

    self.x_mid = (self.x1 + self.x2) / 2
    self.y_mid = (self.y1 + self.y2) / 2
    self.center = Point(self.x_mid, self.y_mid)

    color = "navy"
    if self.has_left_wall:
      color = "black"
    self._win.draw_line(Line(top_left, Point(self.x1, self.y2)), color)
    color = "navy"
    if self.has_right_wall:
      color = "black"
    self._win.draw_line(Line(Point(self.x2, self.y1), bottom_right), color)
    color = "navy"
    if self.has_top_wall:
      color = "black"
    self._win.draw_line(Line(top_left, Point(self.x2, self.y1)), color)
    color = "navy"
    if self.has_bottom_wall:
      color = "black"
    self._win.draw_line(Line(Point(self.x1, self.y2), bottom_right), color)

  def draw_move(self, to_cell, undo=False):
    if self._win == None:
      return

    fill_color = "red"
    if undo:
      fill_color = "gray"
    self._win.draw_line(Line(self.center, to_cell.center), fill_color)
