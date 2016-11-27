""""Paint program by Dave Michell.
"""

from Tkinter import Tk, Canvas, TRUE

b1 = "up"
xold, yold = None, None


def main():
    root = Tk()
    drawing_area = Canvas(root)
    drawing_area.pack()
    drawing_area.bind("<Motion>", motion)
    drawing_area.bind("<ButtonPress-1>", b1down)
    drawing_area.bind("<ButtonRelease-1>", b1up)
    root.mainloop()


def b1down(event):
    global b1  # you only want to draw when the button is down
    b1 = "down"  # because "Motion" events happen -all the time-


def b1up(event):
    global b1, xold, yold
    b1 = "up"
    xold = None  # reset the line when you let go of the button
    yold = None


def motion(event):
    if b1 == "down":
        global xold, yold
        if xold is not None and yold is not None:
            if not abs(event.x - xold) <= 1 and abs(event.y - yold) <= 1:
                print event.x, xold, abs(event.x - xold), "##", event.y, yold, abs(event.y - yold)
            event.widget.create_line(xold, yold, event.x, event.y,
                                     smooth=TRUE)  # here's where you draw it. smooth. neat.
        xold = event.x
        yold = event.y
        # print


if __name__ == "__main__":
    main()