import Tkinter as tk


class Square(object):

    def __init__(self, frame, row, column, value, lines):
        self.lines = lines
        self.label = tk.Label(frame, text=value)
        self.label.grid(row=row * 2 + 1, column=column * 2 + 1)
        self.row = row
        self.column = column
        self.value = None
        self.done = True

    def check_values(self):
        pass

    def test(self):
        for line in self.lines:
            line.set_empty()
