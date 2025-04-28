from tkinter import Tk, BOTH, Canvas


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

        


def main():
    win = Window(800, 600)
    c1 = Cell(1, 30, 30, 60, win)
    c2 = Cell(50, 10, 70, 20, win, True, True, False, False)
    c3 = Cell(80, 90, 90, 130, win, False, False, True, True)
    c1.draw()
    c2.draw()
    c3.draw()
    win.wait_for_close()

main()