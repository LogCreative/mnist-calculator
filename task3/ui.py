from tkinter import *
from PIL import ImageGrab, Image
from colors import getColor

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
        self.startPoint = tuple([0, 0])
        self.strokePoints = []
        self.allStrokes = []

    def mouse_down(self, event):
        self.startPoint = event.x, event.y
        self.strokePoints.clear()

    def draw_line(self, p1, p2, fill="black"):
        self.create_line(p1[0], p1[1], p2[0], p2[1], joinstyle="round", capstyle="round", width=5, fill=fill, tags="inputs")

    def paint(self, event):
        pos = tuple([event.x, event.y])
        self.draw_line(self.startPoint,pos)
        self.startPoint = pos
        self.strokePoints.append(pos)

    def mouse_up(self, event):
        self.allStrokes.append(self.strokePoints.copy())
        self.visualize()
        output_text.set("Prediction")

    def clean(self):
        self.delete("inputs")
        self.allStrokes.clear()

    def draw_stroke(self, stroke, fill="black"):
        prev = stroke[0]
        for _ in range(1,len(stroke)):
            self.draw_line(prev, stroke[_], fill)
            prev = stroke[_]

    def visualize(self):
        self.delete("inputs")
        if visual.get() == "yes": 
            self.allStrokes.sort(key=lambda stroke: min([p[0] for p in stroke]))
            groupDict = {}
            ggid = 0
            for _, stroke in enumerate(self.allStrokes):
                horizontals = [p[0] for p in stroke]
                leftend = min(horizontals)
                rightend = max(horizontals)
                flag = False
                for gid in groupDict.keys():
                    if rightend <= groupDict[gid][2] or \
                        (groupDict[gid][2] - leftend) / (groupDict[gid][2] - groupDict[gid][1]) > 0.1:
                        groupDict[gid][0].append(_)     # contains or mostly overlapped
                        flag = True
                        break
                if flag: continue
                groupDict[ggid] = [[_], leftend, rightend]
                ggid += 1
            for gid in groupDict.keys():
                for strokeId in groupDict[gid][0]:
                    self.draw_stroke(self.allStrokes[strokeId],getColor(gid))
        else: 
            for stroke in self.allStrokes:
                self.draw_stroke(stroke)

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