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
    def __init__(self):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = 
        


def main():
    win = Window(800, 600)
    win.draw_line(Line(Point(89, 104), Point(55, 104)), "black")
    win.wait_for_close()

main()