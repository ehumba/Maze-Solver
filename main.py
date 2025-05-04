from tkinter import Tk, BOTH, Canvas
import time
import random


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze")
        self.__canvas = Canvas()
        self.__canvas.pack()
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    def wait_for_close(self):
        self.__running = True
        while self.__running is True:
            self.redraw()
    def close(self):
        self.__running = False
    def draw_line(self, line, fill_colour):
        line.draw(self.__canvas, fill_colour)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.__point1 = point1
        self.__point2 = point2
    def draw(self, canvas, fill_colour):
        x1, y1 = self.__point1.x, self.__point1.y
        x2, y2 = self.__point2.x, self.__point2.y
        canvas.create_line(
        x1, y1, x2, y2, fill=fill_colour, width=2
)

class Cell:
    def __init__(self, x1, y1, x2, y2, window, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = window
        self.visited = False


    def draw(self):
        top_left = Point(self._x1, self._y1)
        bot_left = Point(self._x1, self._y2)
        top_right = Point(self._x2, self._y1)
        bot_right = Point(self._x2, self._y2)
        left_wall = Line(top_left, bot_left)
        top_wall = Line(top_left, top_right)
        right_wall = Line(top_right, bot_right)
        bottom_wall = Line(bot_left, bot_right)
        if self.has_left_wall == True:
            self._win.draw_line(left_wall, "black")
        if self.has_right_wall == True:
            self._win.draw_line(right_wall,"black")
        if self.has_top_wall == True:
            self._win.draw_line(top_wall,"black")
        if self.has_bottom_wall == True:
            self._win.draw_line(bottom_wall,"black")
        if self.has_left_wall == False:
            self._win.draw_line(left_wall, "#d9d9d9")
        if self.has_right_wall == False:
            self._win.draw_line(right_wall,"#d9d9d9")
        if self.has_top_wall == False:
            self._win.draw_line(top_wall,"#d9d9d9")
        if self.has_bottom_wall == False:
            self._win.draw_line(bottom_wall,"#d9d9d9")
    def draw_move(self, to_cell, undo=False):
        centre1 = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        centre2 = Point((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2)
        move = Line(centre1, centre2)
        if undo == False:
            self._win.draw_line(move, "red")
        if undo == True:
            self._win.draw_line(move, "grey")


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
        seed=False
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not False:
            random.seed(seed)
        self._create_cells()
    def _create_cells(self):
        self._cells = []
        for col in range(self.num_cols):
            column = []
            for row in range(self.num_rows):
                x1 = self.x1 + col * self.cell_size_x
                y1 = self.y1 + row * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y
                cell = Cell(x1, y1, x2, y2, self.win)
                column.append(cell)
                
            self._cells.append(column)
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, i, j):
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self._cells[i][j].draw()
        self._animate()
    def _animate(self):
        self.win.redraw()
        time.sleep(0.03)
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            visit = []
            if j > 0 and not self._cells[i][j - 1].visited:
                visit.append(("down", i, j - 1))
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                visit.append(("up", i, j + 1))
            if i > 0 and not self._cells[i - 1][j].visited:
                visit.append(("left", i - 1, j))
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                visit.append(("right", i + 1, j))
            if len(visit) == 0:
                self._cells[i][j].draw()
                return
            
            direction, ni, nj = random.choice(visit)
            if direction == "up":
                self._cells[i][j].has_top_wall = False
                self._cells[ni][nj].has_bottom_wall = False
            if direction == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[ni][nj].has_left_wall = False
            if direction == "down":
                self._cells[i][j].has_bottom_wall = False
                self._cells[ni][nj].has_top_wall = False
            if direction == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[ni][nj].has_right_wall = False
            
            self._break_walls_r(ni, nj)



def main():
    win = Window(400, 400)
    m1 = Maze(0, 0, 12, 12, 10, 10, win)
    m1._create_cells()
    m1._break_entrance_and_exit()
    m1._break_walls_r(1, 1)
    win.wait_for_close()

main()