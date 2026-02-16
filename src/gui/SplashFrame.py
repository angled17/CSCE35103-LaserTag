import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from gui.PlayerEntryFrame import PlayerEntryFrame


class SplashFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.game = container
        
        self.splash_image = ImageTk.PhotoImage(Image.open('static/logo.jpg').resize((700, 700)), Image.Resampling.LANCZOS)

        # label
        self.img_label = ttk.Label(self, image=self.splash_image)
        self.img_label.grid()

        # show the frame on the container
        self.pack()

        self.after(3000, self.move_to_player_entry)

    
    def move_to_player_entry(self):
        self.game.player_entry_frame = PlayerEntryFrame(self.game, self.game.db, self.game.client_socket)
        self.destroy()


