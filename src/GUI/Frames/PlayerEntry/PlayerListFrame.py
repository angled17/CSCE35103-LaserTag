import tkinter as tk
import ttkbootstrap as ttk

from tkinter.font import Font

class PlayerListFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container, relief="solid", borderwidth=2)

        self.game = main_game
        self.scene = container
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
            t_lab.bind("<Enter>", self.on_label_enter)
            t_lab.bind("<Leave>", self.on_label_exit)
            t_lab.bind("<Button-1>", self.on_label_click)
            t_lab.grid(row=red_index, column=0, padx=10)
            self.player_labels.append(t_lab)

            red_index += 1

        for green_player_id in self.game.green_team:
            t_lab = ttk.Label(self, text=f"{green_player_id} | {self.game.db.get_player_name_from_id(green_player_id)} | {self.game.green_team[green_player_id]}")
            t_lab.bind("<Enter>", self.on_label_enter)
            t_lab.bind("<Leave>", self.on_label_exit)
            t_lab.bind("<Button-1>", self.on_label_click)
            t_lab.grid(row=green_index, column=1, padx=10)
            self.player_labels.append(t_lab)

            green_index += 1


    def on_label_enter(self, event):
        strike_font = Font(font=event.widget['font'])
        strike_font.configure(overstrike=True)
        strike_font.configure(size=10)

        event.widget.config(font=strike_font)

    
    def on_label_exit(self, event):
        og_font = Font(font=event.widget['font'])
        og_font.configure(overstrike=False)
        og_font.configure(size=10)

        event.widget.config(font=og_font)


    def on_label_click(self, event):
        player_id = int(event.widget["text"].split("|")[0][0:-1])
        equip_id = int(event.widget["text"].split("|")[2][1:])

        if equip_id % 2 == 1:
            del self.game.red_team[player_id]
        else:
            del self.game.green_team[player_id]

        self.update_player_list()