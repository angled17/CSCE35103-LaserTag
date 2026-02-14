import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from PIL import Image, ImageTk


class SplashFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        self.splash_image = ImageTk.PhotoImage(Image.open('static/logo.jpg').resize((700, 700), Image.Resampling.LANCZOS))

        # label
        self.img_label = ttk.Label(self, image=self.splash_image)
        self.img_label.grid()

        # show the frame on the container
        self.pack()

        self.after(3000, self.destroy)