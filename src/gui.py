import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk


class SplashFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        self.splash_image = ImageTk.PhotoImage(Image.open('static/logo.jpg').resize((700, 700), Image.Resampling.LANCZOS))

        # label
        self.img_label = ttk.Label(self, image=self.splash_image)
        self.img_label.pack()

        # show the frame on the container
        self.pack()

        self.after(3000, self.destroy)


class PlayerEntryFrame(ttk.Frame):
    def __init__(self, container, database):
        super().__init__(container)

        self.db = database

        # label
        ttk.Style().configure("Red.TLabel", foreground='red')
        self.label = ttk.Label(self, text="Player Entry Frame", style="Red.TLabel")
        self.label.pack()

        self.pack()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Root Window Config
        self.title("Laser Tag!")
        self.geometry('700x700')
        self.resizable(False, False)


