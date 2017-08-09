class Corner(object):

    def __init__(self, row, column, lines):
        self.row = row
        self.column = column
        self.lines = lines
        self.done = False
        for line in self.lines:
            line.add_corner(self)
        self.line_number = None

    def check_values(self):
        if self.done:
            return
        empty = 0
        full = 0
        for line in self.lines:
            if line.is_full:
                full += 1
            if line.is_empty:
                empty += 1
        print self.row, self.column, full, empty, len(self.lines)
        if full + empty == len(self.lines):
            return False
        if full == 2:
            print "two lines so other empty"
            for line in self.lines:
                if not line.is_full:
                    line.set_empty()
                else:
                    print "skip ", line.column, line.row, line.horizontal
                self.done = True
            return True
        elif full == 1:
            if len(self.lines) - empty == 2:
                print "One line and one option"
                for line in self.lines:
                    if not line.is_empty:
                        line.set_full()
                self.done = True
                return True
        else:
            if len(self.lines) - empty == 1:
                print "only one still empty"
                for line in self.lines:
                    if not line.is_full:
                        line.set_empty()
                self.done = True
                return True
        return False
