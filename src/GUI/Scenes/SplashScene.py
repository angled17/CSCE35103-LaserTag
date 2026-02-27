import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from GUI.Scenes.PlayerEntryScene import PlayerEntryScene


class SplashScene(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.game = container

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.game.update_idletasks()

        self.og_image = Image.open('static/logo.jpg')
        self.splash_image = ImageTk.PhotoImage(self.og_image.resize((self.game.winfo_width(), self.game.winfo_height())), Image.Resampling.LANCZOS)

        # label
        self.img_label = ttk.Label(self, image=self.splash_image)
        self.img_label.grid()

        # show the frame on the container
        self.grid(sticky="nsew")

        self.bind("<Configure>", self.on_resize)

        if not any(self.game.debug_flags.values()) or not list(self.game.debug_flags.values()) == [True, False, False]:
            self.after(3000, self.move_to_player_entry)

    
    def move_to_player_entry(self):
        self.game.player_entry_frame = PlayerEntryScene(self.game, self.game.db, self.game.client_socket)
        self.destroy()

    def on_resize(self, event):
        self.game.update_idletasks()

        self.new_img = ImageTk.PhotoImage(self.og_image.resize((event.width, event.height)), Image.Resampling.LANCZOS)
        self.img_label.configure(image=self.new_img)



