import Tkinter as tk


class Line(object):
    NARROW = 5
    WIDE = 10
    full_lines = 0
    series_one = 0
    next_line = 1

    def __init__(self, frame, horizontal, row, column):
        self.horizontal = horizontal
        if horizontal:
            self.canvas = tk.Canvas(frame, width=Line.WIDE,
                                    height=Line.NARROW)
            self.canvas.grid(row=row * 2, column=column * 2 + 1)
        else:
            self.canvas = tk.Canvas(frame, width=Line.NARROW,
                                    height=Line.WIDE)
            self.canvas.grid(row=row * 2 + 1, column=column * 2)
        self.is_full = False
        self.is_empty = False
        self.row = row
        self.column = column
        self.chain = 0
        self.corner1 = None
        self.corner2 = None

    def add_corner(self, corner):
        if self.corner1 is None:
            self.corner1 is corner
        elif self.corner2 is None:
            self.corner2 is corner
        else:
            oops = 1/0
            print(oops)

    def _set_colour(self, colour):
        self.canvas.delete("all")
        if self.horizontal:
            self.canvas.create_rectangle(0, 0, self.WIDE, self.NARROW,
                                         fill=colour)
        else:
            self.canvas.create_rectangle(0, 0, self.NARROW, self.WIDE,
                                         fill=colour)
        self.canvas.update()
        print("set:", self.row, self.column, self.horizontal, colour)

    def set_empty(self):
        self._set_colour("red")
        self.is_empty = True

    def set_full(self):
        global next_line, full_lines
        if self.corner1.line_number is None:
            if self.corner2.line_number is None:
                self.self.line_number = next_line
                next_line += 1
                full_lines += 1
            else:
                self.self.line_number = self.corner2.line_number
        else:
            if self.corner2.line_number is None:
                self.self.line_number = self.corner1.line_number
            if self.corner1.line_number == self.corner2.line_number:
                if full_lines == 1:
                    print("You win")
                    winner = 1/0
                    print(winner)
                else:
                    return False
            else:
                pass

        self._set_colour("green")
        self.is_full = True
        return True

    def reset_chain(self):
        if self.is_full:
            self.chain = 0
