# !/usr/bin/env python3

from tkinter import *
from grid import *

root = Tk()
root.title('Pentrix')
root.minsize(200, 200)
root.geometry('400x400')
root.iconbitmap(r'icon.ico')
root.resizable(True, True)
grid_canvas = ResizableGridCanvas(root,
                                  ColorGrid(25, 25),
                                  width=200,
                                  height=200)
grid_canvas.pack(expand=YES, fill=BOTH)
root.mainloop()
