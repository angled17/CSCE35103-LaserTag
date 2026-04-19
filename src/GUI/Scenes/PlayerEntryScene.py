import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from random import randint

from GUI.Frames.PlayerEntry.NetworkConfigFrame import NetworkConfigFrame
from GUI.Frames.PlayerEntry.AddPlayerFrame import AddPlayerFrame
from GUI.Frames.PlayerEntry.PlayerListFrame import PlayerListFrame

from GUI.Custom.LabeledEntry import LabeledEntry
from Logging.logger import network_message, music_message


class PlayerEntryScene(ttk.Frame):
    def __init__(self, container, database, socket):
        super().__init__(container)

        self.game = container
        self.db = database
        self.socket = socket

        self.counter = 30
        self.delay = 1000

        if self.game.debug_flags["Debug"]:
            self.counter = 1

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

        self.start_game_button = ttk.Button(self, text="Start Game! (F5)", command=self.select_track_and_start_countdown)
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
            self.start_countdown()
        elif event.keysym == "F12":
            self.clear_players()
                

    def select_track_and_start_countdown(self):
        rand_int = randint(1, 8)

        name = f"Track0{rand_int}"
        # name = "Track1"

        track = self.game.music_track_sounds[name]

        self.start_countdown(track, name)

    def start_countdown(self, track, name):
        if self.counter > 0:
            if self.counter == self.game.music_delay + 5:
                self.game.music_channel.play(track)
                music_message(f"Playing {name}")

            self.start_game_button.config(text=f"Starting in {self.counter}...")

            if self.counter == 5:
                self.delay = 1375

            if self.counter == 4:
                self.delay = 1525

            if self.counter == 3:
                self.delay = 1700

            if self.counter == 2:
                self.delay = 1525

            if self.counter == 1:
                self.delay = 1525


            self.counter -= 1
            self.after(self.delay, self.start_countdown, track, name)
        else:
            self.start_game()

    def start_game(self):
        # Initialize self.game.points
        players = []
        for player_id in self.game.red_team:
            players.append(player_id)

        for player_id in self.game.green_team:
            players.append(player_id)

        players.sort()

        for player_id in players:
            self.game.points[player_id] = 0

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
