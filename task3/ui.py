from tkinter import *
from PIL import ImageGrab, Image
from tensorflow.python.ops.gen_math_ops import exp
from colors import getColor
from model import infer

root = Tk()

def grabArea(widget, lt, rb):
    x = root.winfo_rootx() + widget.winfo_x() + lt[0]
    y = root.winfo_rooty() + widget.winfo_y() + lt[1]
    x1 = root.winfo_rootx() + widget.winfo_x() + rb[0]
    y1 = root.winfo_rooty() + widget.winfo_y() + rb[1]
    img = ImageGrab.grab().crop((x,y,x1,y1))
    w = rb[0] - lt[0]
    h = rb[1] - lt[1]
    a = w if w > h else h
    exp_img = Image.new('F',(a,a),0)
    exp_img.paste(img, ((a-w)//2,(a-h)//2))
    exp_img = exp_img.resize((28,28))
    exp_img.show()
    return img

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
        if len(self.strokePoints) > 0:
            self.allStrokes.append(self.strokePoints.copy())
        groupDict = self.grouping()
        for gid in groupDict.keys():
            self.delete("inputs")
            # the bounding box of this group
            gl = groupDict[gid][1]
            gr = groupDict[gid][2]
            gt = 1000
            gb = 0
            for stroke_id in groupDict[gid][0]:
                self.draw_stroke(self.allStrokes[stroke_id])
                gt = min(min(p[1] for p in self.allStrokes[stroke_id]), gt)
                gb = max(max(p[1] for p in self.allStrokes[stroke_id]), gb)
            result = infer(grabArea(c, [gl,gt], [gr,gb]))
            print(result)
        self.visualize()

    def clean(self):
        self.delete("inputs")
        self.allStrokes.clear()

    def draw_stroke(self, stroke, fill="black"):
        prev = stroke[0]
        for _ in range(1,len(stroke)):
            self.draw_line(prev, stroke[_], fill)
            prev = stroke[_]
    
    def grouping(self):
        """
        return a groupDict:
        [0]: the id's belong to this group
        [1]: the leftend of this group
        [2]: the rightend of this group
        """
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
                    # contains or mostly overlapped
                    groupDict[gid][0].append(_)
                    # update the edge point
                    groupDict[gid][1] = min(groupDict[gid][1], leftend)
                    groupDict[gid][2] = max(groupDict[gid][2], rightend)
                    flag = True
                    break
            if flag: continue
            groupDict[ggid] = [[_], leftend, rightend]
            ggid += 1
        return groupDict

    def visualize(self):
        self.delete("inputs")
        if visual.get() == "yes": 
            groupDict = self.grouping()
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