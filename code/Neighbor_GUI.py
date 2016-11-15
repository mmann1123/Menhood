# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 12:44:14 2016

@author: Qi
"""

import Tkinter
win = Tkinter.Tk()
win.title('Mini GIS')
win.bind('<Left>', Mleft)
win.bind('<Right>', Mright)
win.bind('<Up>', Mup)
win.bind('<Down>', Mdown)
canvas = Tkinter.Canvas(win, bg='white', height = 600, width = 800)
canvas.bind("<Button-1>", callback)
canvas.pack(side=Tkinter.LEFT)
frame = Tkinter.Frame(win)

roads = Tkinter.Button(frame, width = 15,text= 'Show Roads',fg="blue")
river = Tkinter.Button(frame, width = 15,text= 'Show Rivers',fg="blue")
checkIn = Tkinter.Button(frame, width = 15,text= 'Check Intersection',fg="blue")                   
shortest = Tkinter.Button(frame, width = 15,text= 'Shortest Path',fg="blue")
reset = Tkinter.Button(frame, width = 15,text= 'Reset',fg="blue")
zoomin = Tkinter.Button(frame, width = 15,text= 'Zoom In',fg="blue")
zoomout = Tkinter.Button(frame, width = 15,text= 'Zoom Out',fg="blue")




roads.pack()
river.pack()
checkIn.pack()
shortest.pack()
reset.pack()
zoomin.pack()
zoomout.pack()
frame.pack(side=Tkinter.RIGHT, fill = Tkinter.BOTH)

win.mainloop()