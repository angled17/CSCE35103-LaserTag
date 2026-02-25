import tkinter as tk
import ttkbootstrap as ttk

class PlayerListFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container, relief="raised", borderwidth=2)

        self.game = main_game

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        

        self.players_label = ttk.Label(self, text="Players - ID | Name | EquipmentID")
        self.players_label.grid(row=0, column=0, padx=10, pady=2, columnspan=2)

        # Red Team - Left
        self.red_team_label = ttk.Label(self, text="Red Team")
        self.red_team_label.grid(row=1, column=0, padx=10, pady=10)

        # Green Team - Right
        self.green_team_label = ttk.Label(self, text="Green Team")
        self.green_team_label.grid(row=1, column=1, padx=10, pady=10)