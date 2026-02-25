import tkinter as tk
import ttkbootstrap as ttk

class PlayerListFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container, relief="raised", borderwidth=2)

        self.game = main_game
        self.player_labels = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.players_label = ttk.Label(self, text="Players: ID | Name | EquipmentID")
        self.players_label.grid(row=0, column=0, padx=10, pady=2, columnspan=2)

        # Red Team - Left
        self.red_team_label = ttk.Label(self, text="Red Team")
        self.red_team_label.grid(row=1, column=0, padx=10, pady=10)

        # Green Team - Right
        self.green_team_label = ttk.Label(self, text="Green Team")
        self.green_team_label.grid(row=1, column=1, padx=10, pady=10)

    
    def update_player_list(self):
        # Destory Player Labels
        for l in self.player_labels:
            l.destroy()

        red_index = 2
        green_index = 2
        

        for red_player_id in self.game.red_team:
            t_lab = ttk.Label(self, text=f"{red_player_id} | {self.game.db.get_player_name_from_id(red_player_id)} | {self.game.red_team[red_player_id]}")
            t_lab.grid(row=red_index, column=0, padx=10)
            self.player_labels.append(t_lab)

            red_index += 1

        for green_player_id in self.game.green_team:
            t_lab = ttk.Label(self, text=f"{green_player_id} | {self.game.db.get_player_name_from_id(green_player_id)} | {self.game.green_team[green_player_id]}")
            t_lab.grid(row=green_index, column=1, padx=10)
            self.player_labels.append(t_lab)

            green_index += 1