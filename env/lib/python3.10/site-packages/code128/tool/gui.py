#! /usr/bin/env python3

# Copyright (c) 2014-2015 Felix Knopf <felix.knopf@arcor.de>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License in the LICENSE.txt for more details.
#

import code128
from .ModifiedMixin import ModifiedMixin

try:
    from tkinter import *
    import tkinter.filedialog as filedialog
    from PIL import ImageTk
except ImportError:
    raise ImportError("Please ensure, that tkinter and PIL are available")


filetypes = [("Supported Formats",
              "*.bmp *.dib *.gif *.im *.jpg *.jpe *.jpeg *.pcx *.png *.pbm " \
              "*.pgm *.ppm *.tif *.tiff *.xbm *.xpm"), #*.svg"),
             ("All Files", "*") ]

class TextField(ModifiedMixin, Text):
    def __init__(self, *a, **b):
        Text.__init__(self, *a, **b)
        self._init()

    def beenModified(self, event=None):
        cApply()


def updateDisplay():
    global disp, photo
    
    for i in disp.find_all(): disp.delete(i)
    disp.create_image((0,0), image=photo, anchor=NW)
    disp.update_idletasks()

def scaleImage(rawImage):
    global w,h
    
    scaledImage = rawImage
    scaledImage.thumbnail((w*0.3,h*0.1))
    return ImageTk.PhotoImage(scaledImage)  
            
def cApply():
    global result, T, photo
    
    result = code128.image(T.get("1.0", 'end-1c'))
    photo = scaleImage(result.convert("RGB"))
    updateDisplay() 
    
def cSave():
    global result
    cApply()
    file = filedialog.asksaveasfilename(parent=disp, title="Save Barcode",
                                        filetypes=filetypes)
    result.save(file)

def gui_main(): 
    global w,h,T,disp
    
    root = Tk()
    root.title("Code128")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()

    # Barcode Viewer
    disp = Canvas(root, width=w*0.3, height=h*0.1)
    disp.grid(row=0, column=0, padx=20, pady=20)

    # Info Text
    l1 = Label(root, text="Type the text you want to enconde below.")
    l1.grid(row=0, column=1, pady=10)

    # Input Box
    T = TextField(root, width=60, height=8)
    T.grid(row=1, column=1)

    # Control Buttons
    subWnd1 = Frame(root)
    subWnd1.grid(row=2, column=1, padx=30, pady=30)

    bApply  = Button(subWnd1, text="Apply", width=10, command=cApply)
    bSave   = Button(subWnd1, text="Save", width=10, command=cSave)
    bCancel = Button(subWnd1, text="Cancel",width=10,
                     command=lambda: root.destroy()) 

    bApply.grid(column=0, row=0, padx=10)
    bSave.grid(column=1, row=0, padx=10)
    bCancel.grid(column=2, row=0, padx=10)

    root.mainloop()

if __name__ == "__main__": gui_main()
