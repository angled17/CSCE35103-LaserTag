import tkinter as tk
import ttkbootstrap as ttk


class PlayersFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container, relief="raised", borderwidth=2)

        self.game = main_game
        self.scene = container
        self.player_labels = []

        # self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)


        ttk.Label(self, text="Players", relief="raised", borderwidth=2, anchor="center").grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 4), columnspan=2)
        ttk.Label(self, text="Red Team", relief="raised", borderwidth=2, anchor="center").grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Label(self, text="Green Team", relief="raised", borderwidth=2, anchor="center").grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.update_player_list()


    def update_player_list(self):
        # Destory Player Labels
        for l in self.player_labels:
            l.destroy()

        red_index = 2
        green_index = 2
        

        for red_player_id in self.game.red_team:
            t_lab = ttk.Label(self, text=f"{self.game.db.get_player_name_from_id(red_player_id)} ({self.game.red_team[red_player_id]}): points_placeholder")
            # t_lab.bind("<Enter>", self.on_label_enter)
            # t_lab.bind("<Leave>", self.on_label_exit)
            # t_lab.bind("<Button-1>", self.on_label_click)
            t_lab.grid(row=red_index, column=0, padx=10)
            self.player_labels.append(t_lab)

            red_index += 1

        for green_player_id in self.game.green_team:
            t_lab = ttk.Label(self, text=f"{self.game.db.get_player_name_from_id(green_player_id)} ({self.game.green_team[green_player_id]}): points_placeholder")
            # t_lab.bind("<Enter>", self.on_label_enter)
            # t_lab.bind("<Leave>", self.on_label_exit)
            # t_lab.bind("<Button-1>", self.on_label_click)
            t_lab.grid(row=green_index, column=1, padx=10)
            self.player_labels.append(t_lab)

            green_index += 1 

        