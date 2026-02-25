import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *

from GUI.Frames.NetworkConfigFrame import NetworkConfigFrame
from GUI.Frames.AddPlayerFrame import AddPlayerFrame
from GUI.Frames.PlayerListFrame import PlayerListFrame

from GUI.Custom.LabeledEntry import LabeledEntry
from Logging.logger import general_message, network_message


class PlayerEntryScene(ttk.Frame):
    def __init__(self, container, database, socket):
        super().__init__(container, relief="raised", borderwidth=5)

        self.game = container
        self.db = database
        self.socket = socket

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.network_frame = NetworkConfigFrame(self, self.game)
        self.network_frame.grid(row=0, column=0, rowspan=2, columnspan=2, padx=10, pady=5)

        self.add_player_frame = AddPlayerFrame(self, self.game)
        self.add_player_frame.grid(row=0, column=2, rowspan=2, columnspan=3, padx=10, pady=5)

        self.start_game_button = ttk.Button(self, text="Start Game!", command=self.start_game)
        self.start_game_button.grid(row=2, column=0, columnspan=5, pady=10)

        self.player_list_frame = PlayerListFrame(self, self.game)
        self.player_list_frame.grid(row=3, column=0, columnspan=5, padx=10, pady=5)

        self.bind("<Key>", self.key_listener)
        self.focus_set()

        self.grid(row=0, column=0, sticky="n")

    
    

    
    def update_player_list(self):
        # Destory Player Labels
        for l in self.player_labels:
            l.destroy()

        # Update Red
        red_index = self.start_list_row
        green_index = self.start_list_row

        for red_player_id in self.game.red_team:
            t_lab = ttk.Label(self, text=f"{red_player_id} | {self.db.get_player_from_id(red_player_id)} | {self.game.red_team[red_player_id]}")
            t_lab.grid(row=red_index, column=1, padx=5)
            self.player_labels.append(t_lab)

            red_index += 1

        for green_player_id in self.game.green_team:
            t_lab = ttk.Label(self, text=f"{green_player_id} | {self.db.get_player_from_id(green_player_id)} | {self.game.green_team[green_player_id]}")
            t_lab.grid(row=green_index, column=3, padx=5)
            self.player_labels.append(t_lab)

            green_index += 1


    def update_network(self):
        addr = self.network_addr.get().split(":")

        self.game.addr_from = addr[0]
        self.game.addr_from_port = int(addr[1])

        self.game.send_to_location = (addr[0], int(addr[1]))


    def key_listener(self, event):
        if event.keysym == "F5":
            self.start_game()


    def start_game(self):
        self.socket.sendto("202".encode(), self.game.send_to_location)
        self.game.start_game()
