import Tkinter
from PIL import Image, ImageTk
import numpy
import time


class mainWindow():
    times = 1
    timestart = time.clock()
    data = numpy.array(numpy.random.random((400, 500)) * 100, dtype=int)

    def __init__(self):
        self.root = Tkinter.Tk()
        self.frame = Tkinter.Frame(self.root, width=500, height=400)
        self.frame.pack()

        self.canvas = Tkinter.Canvas(self.frame, width=500, height=400)
        self.canvas.place(x=-2, y=-2)
        self.root.after(0, self.start)  # INCREASE THE 0 TO SLOW IT DOWN
        self.root.mainloop()


def start(self):
    global data
    self.im = Image.fromstring('L', (self.data.shape[1],
                                     self.data.shape[0]), self.data.astype('b').tostring())
    self.photo = ImageTk.PhotoImage(image=self.im)
    self.canvas.create_image(0, 0, image=self.photo, anchor=Tkinter.NW)
    self.root.update()
    self.times += 1
    if self.times % 33 == 0:
        print "%.02f FPS" % (self.times / (time.clock() - self.timestart))
    self.root.after(10, self.start)
    self.data = numpy.roll(self.data, -1, 1)


if __name__ == '__main__':
    x = mainWindow()
