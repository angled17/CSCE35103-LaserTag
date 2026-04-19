import tkinter as tk
import ttkbootstrap as ttk


class PlayersFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container, relief="raised", borderwidth=2)

        self.game = main_game
        self.scene = container
        self.player_labels = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        sum_red_team = 0
        sum_green_team = 0

        for id in self.game.points:
            if id % 2 == 1:
                sum_red_team += self.game.points[id] 
            else:
                sum_green_team += self.game.points[id]


        ttk.Label(self, text="Current Scores", anchor="center").grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 8), columnspan=3)

        self.red_team_points = ttk.Label(self, text=f"Red Team: {sum_red_team}", anchor="center")
        self.red_team_points.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        separator_row_span = max(len(self.game.red_team), len(self.game.green_team)) + 1
        ttk.Separator(self, orient="vertical").grid(row=1, column=1, sticky="ns", rowspan=separator_row_span)

        self.green_team_points = ttk.Label(self, text=f"Green Team: {sum_green_team}", anchor="center")
        self.green_team_points.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        
        self.update_player_list()


    def update_player_list(self):
        # Destory Sum Labels
        self.red_team_points.destroy()
        self.green_team_points.destroy()

        # Destory Player Labels
        for l in self.player_labels:
            l.destroy()

        # Add Total Points
        sum_red_team = 0
        sum_green_team = 0

        for id in self.game.points:
            if id % 2 == 1:
                sum_red_team += self.game.points[id] 
            else:
                sum_green_team += self.game.points[id]

        self.red_team_points = ttk.Label(self, text=f"Red Team: {sum_red_team}", anchor="center")
        self.red_team_points.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.green_team_points = ttk.Label(self, text=f"Green Team: {sum_green_team}", anchor="center")
        self.green_team_points.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # Add Individual Points
        red_index = 2
        green_index = 2

        sorted_points_reversed = sorted(self.game.points, key=self.game.points.get, reverse=True)

        red_team_ids = [id for id in sorted_points_reversed if id % 2 == 1]
        green_team_ids = [id for id in sorted_points_reversed if id % 2 == 0]
    

        for red_player_id in red_team_ids:
            t_lab = ttk.Label(self, text=f"{self.game.db.get_player_name_from_id(red_player_id)}: {self.game.points[red_player_id]}")
            # t_lab.bind("<Enter>", self.on_label_enter)
            # t_lab.bind("<Leave>", self.on_label_exit)
            # t_lab.bind("<Button-1>", self.on_label_click)
            t_lab.grid(row=red_index, column=0, padx=10)
            self.player_labels.append(t_lab)

            red_index += 1

        for green_player_id in green_team_ids:
            t_lab = ttk.Label(self, text=f"{self.game.db.get_player_name_from_id(green_player_id)}: {self.game.points[green_player_id]}")
            # t_lab.bind("<Enter>", self.on_label_enter)
            # t_lab.bind("<Leave>", self.on_label_exit)
            # t_lab.bind("<Button-1>", self.on_label_click)
            t_lab.grid(row=green_index, column=2, padx=10)
            self.player_labels.append(t_lab)

            green_index += 1 

        