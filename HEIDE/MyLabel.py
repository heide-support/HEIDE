# code taken from
# http://stackoverflow.com/questions/7960600/python-tkinter-display-animated-gif-using-pil

from tkinter import *
from PIL import Image, ImageTk


class MyLabel(Label):
    def __init__(self, master, filename):
        self.im = Image.open(filename)
        self.seq =  []
        try:
            while 1:
                self.seq.append(self.im.copy())
                self.im.seek(len(self.seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = self.im.info['duration']
        except KeyError:
            self.delay = 100

        first = self.seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        temp = self.seq[0]
        for image in self.seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)