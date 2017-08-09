import Tkinter as tk

from corner import Corner
from line import Line
from square import Square
from value_square import ValueSquare


class Board(object):
    matrix = []
    vertical_walls = []
    horizontal_walls = []

    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()

        top = tk.Frame(frame)
        top.pack()

        bottom = tk.Frame(frame)
        bottom.pack()
        stats_button = tk.Button(bottom, text="Stats", command=self.stats)
        stats_button.grid(row=0, column=0)
        next_button = tk.Button(bottom, text="Next", command=self.check)
        next_button.grid(row=0, column=1)

        values = self.read_values()
        print values
        self.max_row = len(values)
        self.max_col = len(values[0])

        self.setup_walls(top)
        self.setup_squares(top, values)
        self.setup_corners()

    def read_values(self):
        values = []
        max_col = None
        with open("easy1.csv", "r") as f:
            for line in f:
                line = line.strip()
                parts = line.split(",")
                if max_col is None:
                    max_col = len(parts)
                else:
                    if max_col != len(parts):
                        raise Exception("Incorrect length")
                values.append(parts)
        return values

    def setup_walls(self, frame):
        for row in range(self.max_row):
            vertical_list = []
            horizontal_list = []
            for column in range(self.max_col):
                # above
                horizontal_list.append(Line(frame, True, row, column))
                # left
                vertical_list.append(Line(frame, False, row, column))
            # right
            vertical_list.append(Line(frame, False, row, self.max_col))
            self.vertical_walls.append(vertical_list)
            self.horizontal_walls.append(horizontal_list)

        horizontal_list = []
        for column in range(self.max_col):
            # below
            horizontal_list.append(Line(frame, True, self.max_row, column))
        self.horizontal_walls.append(horizontal_list)

    def setup_squares(self, frame, values):
        for row in range(self.max_row):
            row_list = []
            for column in range(self.max_col):
                if values[row][column].isdigit():
                    s = ValueSquare(frame, row, column,
                                    int(values[row][column]),
                                    [self.horizontal_walls[row][column],
                                     self.vertical_walls[row][column],
                                     self.horizontal_walls[row+1][column],
                                     self.vertical_walls[row][column+1]])
                else:
                    s = Square(frame, row, column, "",
                               [self.horizontal_walls[row][column],
                                self.vertical_walls[row][column],
                                self.horizontal_walls[row+1][column],
                                self.vertical_walls[row][column+1]])
                row_list.append(s)
            self.matrix.append(row_list)

    def setup_corners(self):
        self.corners = []
        for row in range(self.max_row+1):
            for column in range(self.max_col+1):
                lines = []
                if column > 0:
                    lines.append(self.horizontal_walls[row][column-1])
                if row > 0:
                    lines.append(self.vertical_walls[row-1][column])
                if column < self.max_col:
                    lines.append(self.horizontal_walls[row][column])
                if row < self.max_row:
                    lines.append(self.vertical_walls[row][column])
                self.corners.append(Corner(row, column, lines))

    def stats(self):
        not_done = 0
        for row in range(self.max_row):
            for column in range(self.max_col):
                if not self.matrix[row][column].done:
                    not_done += 1
        print "not done: ", not_done

    def check(self):
        print "==="
        for row in range(self.max_row):
            for column in range(self.max_col):
                if self.matrix[row][column].check_values():
                    return
        for corner in self.corners:
            if corner.check_values():
                return
        # diagonal 0,3

    def check_three_three(self):
        for row in range(self.max_row-1):
            for column in range(self.max_col):
                if self.matrix[row][column].value == 3:
                    if self.matrix[row+1][column].value == 3:
                        print "3 3 detected horizontal", row, column
                        self.horizontal_walls[row][column].set_full()
                        self.horizontal_walls[row + 1][column].set_full()
                        self.horizontal_walls[row + 2][column].set_full()
        for row in range(self.max_row):
            for column in range(self.max_col - 1):
                if self.matrix[row][column].value == 3:
                    if self.matrix[row][column + 1].value == 3:
                        print "3 3 detected vertical", row, column
                        self.vertical_walls[row][column].set_full()
                        self.vertical_walls[row][column + 1].set_full()
                        self.vertical_walls[row][column + 2].set_full()


# Allow the class to run stand-alone.
if __name__ == "__main__":
    # MyApp1().mainloop()

    root = tk.Tk()

    app = Board(root)
    app.check_three_three()
    # app.check()
    # print "============="
    # app.check()

    root.mainloop()
