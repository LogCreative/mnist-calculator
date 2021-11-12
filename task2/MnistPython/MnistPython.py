# Pythononnet basic example is from 
# https://github.com/pythonnet/pythonnet/blob/master/demo/helloform.py

import clr
SWF = clr.AddReference("System.Windows.Forms")
print (SWF.Location)
import System.Windows.Forms as WinForms
from System.Drawing import Size, Point, Bitmap, Graphics, Color, Pen
from System.Drawing.Drawing2D import LineCap
from System.Collections.Generic import List, IEnumerable
from System import Single, Convert
from collections.abc import Iterable

import sys
assembly_path = '..\\Model\\bin\\x64\\Release'
sys.path.append(assembly_path)

clr.AddReference("Model")
import Model

class HelloApp(WinForms.Form):
    """A simple hello world app that demonstrates the essentials of
       winforms programming and event-based programming in Python."""

    def __init__(self):
        self.Text = "Hand Writing Digit Recognition Based on Python"
        self.ClientSize = Size(884,613)

        self.model = Model.Mnist()

        # Create the painting area
        self.writeArea = WinForms.PictureBox()
        self.writeArea.Location = Point(9,9)
        self.writeArea.Size = Size(562,540)
        self.writeArea.Image = Bitmap(self.writeArea.Width, self.writeArea.Height)
        self.writeArea.MouseDown += self.writeArea_MouseDown
        self.writeArea.MouseMove += self.writeArea_MouseMove
        self.writeArea.MouseUp += self.writeArea_MouseUp
        self.graphics = Graphics.FromImage(self.writeArea.Image)
        self.startPoint = Point(0,0)
        self.ImageSize = 28

        # Create the label
        self.outputText = WinForms.Label()
        self.outputText.Location = Point(580,9)
        self.outputText.Size = Size(273,266)

        # Create the button
        self.button1 = WinForms.Button()
        self.button1.Location = Point(580,444)
        self.button1.Size = Size(272,105)
        self.button1.Text = "Erase"
        self.button1.Click += self.clean_click

        # Add the controls
        self.Controls.Add(self.writeArea)
        self.Controls.Add(self.outputText)
        self.Controls.Add(self.button1)

        self.graphics.Clear(Color.White)
        self.writeArea.Invalidate()
        self.outputText.Text = ""

    def clean_click(self, sender, args):
        self.graphics.Clear(Color.White)
        self.writeArea.Invalidate()
        self.outputText.Text = ""

    def writeArea_MouseDown(self, sender, args):
        if args.Button == WinForms.MouseButtons.Left:
            self.startPoint = args.Location

    def writeArea_MouseMove(self, sender, args):
        if args.Button == WinForms.MouseButtons.Left:
            penStyle = Pen(Color.Black, 40)
            penStyle.StartCap = LineCap.Round
            penStyle.EndCap = LineCap.Round
            self.graphics.DrawLine(penStyle, self.startPoint, args.Location)
            self.writeArea.Invalidate()
            self.startPoint = args.Location

    def writeArea_MouseUp(self, sender, args):
        if args.Button == WinForms.MouseButtons.Left:
            clonedBmp = Bitmap(self.writeArea.Image, self.ImageSize, self.ImageSize)
            image = List[Single](self.ImageSize * self.ImageSize)
            for y in range(0, self.ImageSize):
                for x in range(0, self.ImageSize):
                    color = clonedBmp.GetPixel(x,y)
                    avg = (color.R + color.G + color.B) / 3.0
                    rev = 0.5 - avg / 255
                    image.Add(Single(rev))
            imageWrapper = List[IEnumerable[Single]]()
            imageWrapper.Add(image)
            inferResult = self.model.Infer(imageWrapper)
            # Get the first of the first in IEnumerator<IEnumerator<T>>
            # https://stackoverflow.com/a/497275
            enumer = inferResult.GetEnumerator()
            enumer.MoveNext()
            enumer = enumer.Current.GetEnumerator()
            enumer.MoveNext()
            self.outputText.Text = Convert.ToString(enumer.Current)

    def run(self):
        WinForms.Application.Run(self)


def main():
    form = HelloApp()
    print ("form created")
    app = WinForms.Application
    print ("app referenced")
    app.Run(form)


if __name__ == '__main__':
    main()