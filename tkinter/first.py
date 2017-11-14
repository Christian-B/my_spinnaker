import Tkinter as tk


def ex1():
    root1 = tk.Tk()
    label = tk.Label(root1, text='our label widget')
    entry = tk.Entry(root1)
    label.pack(side=tk.TOP)
    entry.pack()
    root1.mainloop()


def ex2():
    # firstTkinter2.py
    top = tk.Tk()
    lab = tk.Label(top, text="Hello World")
    lab.pack()
    # Give the window a title.
    top.title("My App")
    # Change the minimum size.
    top.minsize(400, 400)
    # Change the background colour.
    top.configure(bg="green")
    # Run the widget.
    top.mainloop()


# Extend the Frame class, to inherit
# the mainloop function.
class MyApp1(tk.Frame):

    def __init__(self, master=None):
        # Construct the Frame object.
        tk.Frame.__init__(self, master)
        self.pack()
        self.lab = tk.Label(self, text="My Button:")
        self.lab.pack()
        self.b = tk.Button(self, text="Hello", command=self.hello)
        self.b.pack()

    # Function called when the button
    # is pressed.
    def hello(self):
        print "Hello"


class App2:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()

        self.button = tk.Button(
            frame, text="QUIT", fg="red", command=frame.quit
        )
        self.button.pack(side=tk.LEFT)

        self.hi_there = tk.Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=tk.LEFT)

    def say_hi(self):
        print "hi there, everyone!"


class App3:
    narrow = 10
    wide = 20
    max_row = 6
    max_col = 4

    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()

        matrix = []
        for row in range(self.max_row):
            row_list = []
            # left
            canvas = tk.Canvas(frame, width=self.narrow, height=self.wide)
            canvas.grid(row=row * 2 + 1, column=0)
            canvas.create_rectangle(0, 0, self.narrow, self.wide, fill="blue")
            for column in range(self.max_col):
                # above
                canvas = tk.Canvas(frame, width=self.wide, height=self.narrow)
                canvas.grid(row=row * 2, column=column * 2 + 1)
                canvas.create_rectangle(0, 0, self.wide, self.narrow,
                                        fill="blue")
                # right
                canvas = tk.Canvas(frame, width=self.narrow, height=self.wide)
                canvas.grid(row=row * 2 + 1, column=column * 2 + 2)
                canvas.create_rectangle(0, 0, self.narrow, self.wide,
                                        fill="blue")
                entry = tk.Entry(frame, width=2)
                entry.grid(row=row * 2 + 1, column=column * 2 + 1)
                entry.insert(tk.END, "{}".format(row + column))
                row_list.append(entry)
        matrix.append(row_list)
        for column in range(self.max_col):
            # below
            canvas = tk.Canvas(frame, width=self.wide, height=self.narrow)
            canvas.grid(row=self.max_row * 2 + 1, column=column * 2 + 1)
            canvas.create_rectangle(0, 0, self.wide, self.narrow, fill="blue")


# Allow the class to run stand-alone.
if __name__ == "__main__":
    # MyApp1().mainloop()

    root = tk.Tk()

    app = App3(root)

    root.mainloop()
