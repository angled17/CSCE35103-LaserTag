import tkinter as tk
import ttkbootstrap as ttk


class PlayersFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container, relief="raised", borderwidth=2)

        self.game = main_game
        self.scene = container

        # self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text="Red Team", relief="raised", borderwidth=2).grid(row=0, column=0, sticky="nsew")
        ttk.Label(self, text="Green Team", relief="raised", borderwidth=2).grid(row=0, column=1, sticky="nsew")