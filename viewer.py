#!/usr/bin/env python
"""
@@@  @@@  @@@@@@   @@@@@@@   @@@@@@@@  @@@@@@@@@@    @@@@@@
@@@  @@@  @@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@@@@  @@@@@@@@
@@!  @@@      @@@  @@!  @@@  @@!       @@! @@! @@!  @@!  @@@
!@!  @!@      @!@  !@!  @!@  !@!       !@! !@! !@!  !@!  @!@
@!@!@!@!  @!@!!@   @!@  !@!  @!!!:!    @!! !!@ @!@  @!@!@!@!
!!!@!!!!  !!@!@!   !@!  !!!  !!!!!:    !@!   ! !@!  !!!@!!!!
!!:  !!!      !!:  !!:  !!!  !!:       !!:     !!:  !!:  !!!
:!:  !:!      :!:  :!:  !:!  :!:       :!:     :!:  :!:  !:!
::   :::  :: ::::   :::: ::   :: ::::  :::     ::   ::   :::
 :   : :   : : :   :: :  :   : :: ::    :      :     :   : :


A simple image viewer in python.

* requires Pillow ( https://pypi.python.org/pypi/Pillow/ ).

"""
from PIL import Image
from PIL import ImageTk

from tkinter import Frame, Button, Label
from tkinter import LEFT, TOP, BOTH

from tkinter import filedialog


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Simple Image Viewer')

        self.filename = None
        self.zoom = 1
        self.img = None

        self.perc = 0.1  # increment of the zoom

        out_fram = Frame(self, width=300, height=16)
        fram = Frame(self)
        self.btOpen = Button(fram, text="Open file", command=self.open)
        self.btOpen.pack(side=LEFT)
        Button(fram, text="Close file", command=self.close).pack(side=LEFT)
        Button(fram, text="Zoom +", command=self.zoom_up).pack(side=LEFT)
        Button(fram, text="Zoom -", command=self.zoom_down).pack(side=LEFT)
        out_fram.pack(side=TOP, fill=BOTH)
        fram.place(in_=out_fram, anchor="c", relx=.5, rely=.5)
        #
        # bind keyboard
        #
        self.master.bind('o', self.open)
        self.master.bind('c', self.close)
        self.master.bind('+', self.zoom_up)
        self.master.bind('-', self.zoom_down)
        # indicates the number of the picture

        self.la = Label(self)
        self.la.pack()

        # <Button>: both buttons <Double-1>: double right click
        self.la.bind("<Button-1>", self.on_click)

        # center window
        pRight = int((self.winfo_screenmmwidth() - self.winfo_reqwidth()) / 2)
        pDown = int((self.winfo_screenmmheight() - self.winfo_reqheight()) / 2)
        self.place(cnf={"x": pRight, "y": pDown})

        self.pack()

    def on_click(self, event):
        print("Mouse position: (%s %s)" % (event.x, event.y))

    def _update_img(self, im):
        if im.mode == "1":
            # bitmap image
            img = ImageTk.BitmapImage(im, foreground="white")
        else:
            # photo image
            img = ImageTk.PhotoImage(im)

        # img._PhotoImage__photo.write("ttt.png")
        self.la.config(image=img,
                       bg="#000000",
                       width=img.width(),
                       height=img.height())
        self.la.image = img

    def close(self, _event=None):
        self.filename = None
        self.img = None
        self.la.config(image="")

    def open(self, _event=None):
        filename = filedialog.askopenfilename()
        if filename != "":
            self.img = Image.open(filename)
            self.filename = filename
        self._update_img(self.img)

    def resize(self, img, zoom=0):
        width, height = img.width, img.height
        img = img.resize((int(self.zoom * width), int(self.zoom * height)),
                         Image.ANTIALIAS)
        return img

    def _zoom(self, _event=None):
        if self.img is None:
            return
        img = self.img.copy()
        img = self.resize(img, self.zoom)
        self._update_img(img)

    def zoom_up(self, _event=None):
        self.zoom = self.zoom + self.perc
        if self.zoom > 5:
            self.zoom = 5
        self._zoom()

    def zoom_down(self, _event=None):
        self.zoom = self.zoom - self.perc
        if self.zoom < 0.1:
            self.zoom = 0.1
        self._zoom()


if __name__ == "__main__":
    app = App()
    app.mainloop()
