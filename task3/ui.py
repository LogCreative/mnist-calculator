from tkinter import *
root = Tk()

class WriteArea(Canvas):
    def __init__(self, master, **kwargs):
        Canvas.__init__(self, master, kwargs)
        self.bind("<Button-1>", self.mouse_down)
        self.bind("<B1-Motion>", self.paint)
        self.bind("<B1-ButtonRelease>", self.mouse_up)
        self.startPoint = 0, 0

    def mouse_down(self, event):
        self.startPoint = event.x, event.y

    def paint(self, event):
        self.create_line(self.startPoint,
                         event.x, 
                         event.y, 
                         joinstyle="round", 
                         width=3,
                         fill="black")
        self.startPoint = event.x, event.y

    def mouse_up(self, event):
        print("Mouse released at ", event.x, event.y)

c = WriteArea(root, width=600, height=200, bg="white")
c.pack()

def clean():
    print("Will be cleaned.")

b = Button(root, width=20, height=5, text="Erase", command=clean)
b.pack()

output_text = Label(root, width=40, height=5)
output_text.pack()

s = Checkbutton(root, width=20, height=5, text="Visualize Stroke Groups")
s.pack()

root.mainloop()