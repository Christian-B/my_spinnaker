from square import Square


class ValueSquare(Square):

    def __init__(self, frame, row, column, value, lines):
        Square.__init__(self, frame, row, column, str(value), lines)
        self.value = int(value)
        self.done = False

    def check_values(self):
        if self.done:
            return False
        max = 4
        min = 0
        for line in self.lines:
            if line.is_full:
                min += 1
            if line.is_empty:
                max -= 1
        if max == min:
            return  # all done
            self.done = True
        if self.value == min:
            print(self.row, self.column, "Rest empty")
            for line in self.lines:
                if not line.is_full:
                    line.set_empty()
            self.done = True
            return True
        if self.value == max:
            print(self.row, self.column, "Rest full")
            for line in self.lines:
                if not line.is_empty:
                    line.set_full()
            self.done = True
            return True
        return False
