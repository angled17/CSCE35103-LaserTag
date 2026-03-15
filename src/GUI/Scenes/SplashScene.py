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

        # label
        self.img_label = ttk.Label(self, image=self.game.splash_image)
        self.img_label.grid()

        # show the frame on the container
        self.grid(sticky="nsew")

        self.bind("<Configure>", self.on_resize)

        if not any(self.game.debug_flags.values()) or not list(self.game.debug_flags.values()) == [True, False, False]:
            time_after = 3000

            if self.game.debug_flags["Debug"]:
                time_after = 500

            self.after(time_after, self.move_to_player_entry)

    
    def move_to_player_entry(self):
        self.game.player_entry_frame = PlayerEntryScene(self.game, self.game.db, self.game.client_socket)
        self.destroy()

    def on_resize(self, event):
        self.game.update_idletasks()

        self.game.splash_image = ImageTk.PhotoImage(self.game.logo_image.resize((event.width, event.height)), Image.Resampling.LANCZOS)
        self.img_label.configure(image=self.game.splash_image)



