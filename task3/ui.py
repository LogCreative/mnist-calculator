from tkinter import *
from PIL import ImageGrab, Image

root = Tk()

def getter(widget):
    x = root.winfo_rootx() + widget.winfo_x()
    y = root.winfo_rooty() + widget.winfo_y()
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    return ImageGrab.grab().crop((x,y,x1,y1))

class WriteArea(Canvas):
    def __init__(self, master, **kwargs):
        Canvas.__init__(self, master, kwargs)
        self.bind("<Button-1>", self.mouse_down)
        self.bind("<B1-Motion>", self.paint)
        self.bind("<B1-ButtonRelease>", self.mouse_up)
        self.startPoint = 0, 0
        self.strokePoints = []
        self.allStrokes = []

    def mouse_down(self, event):
        self.startPoint = event.x, event.y
        self.strokePoints.clear()

    def paint(self, event):
        self.create_line(self.startPoint[0],
                         self.startPoint[1],
                         event.x, 
                         event.y, 
                         joinstyle="round", 
                         capstyle="round",
                         width=5,
                         fill="black",
                         tags="inputs")
        pos = tuple([event.x, event.y])
        self.startPoint = pos
        self.strokePoints.append(pos)

    def mouse_up(self, event):
        self.allStrokes.append(self.strokePoints)
        self.visualize()
        output_text.set("Prediction")

    def clean(self):
        self.delete("inputs")

    def visualize(self):
        if visual.get() == "yes": 
            print("I will visualize")
        else: 
            print("I will recover")

c = WriteArea(root, width=600, height=200, bg="white")
c.pack()

output_text = StringVar()

def clean():
    c.clean()
    output_text.set("")

b = Button(root, width=20, height=5, text="Erase", command=clean)
b.pack()

r = Label(root, width=40, height=5, textvariable=output_text)
r.pack()

visual = StringVar()
visual.set("no")

def visualize():
    c.visualize()

s = Checkbutton(root, width=20, height=5, variable=visual, text="Visualize Stroke Groups", onvalue="yes", offvalue="no", command=visualize)
s.pack()

root.mainloop()