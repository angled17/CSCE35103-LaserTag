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
        super().__init__(container)

        self.game = container
        self.db = database
        self.socket = socket

        self.bind_all("<Button-1>", self.widget_focus)

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


    def widget_focus(self, event):
        if not isinstance(event.widget, str):
            event.widget.focus_set()

    def key_listener(self, event):
        if event.keysym == "F5":
            self.start_game()
        elif event.keysym == "F12":
            self.clear_players()
                

    def start_game(self):
        self.socket.sendto("202".encode(), self.game.send_to_location)
        self.game.start_game()

    
    def clear_players(self):
        self.game.red_team.clear()
        self.game.green_team.clear()
        self.update_list()


    def update_list(self):
        self.player_list_frame.update_player_list()

    
    def broadcast(self, msg):
        self.socket.sendto(msg.encode(), self.game.send_to_location)
        network_message(f"Broadcasted {msg} to {self.game.send_to_location[0]}:{self.game.send_to_location[1]}")
