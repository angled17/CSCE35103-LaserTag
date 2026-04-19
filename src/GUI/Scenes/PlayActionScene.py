import socket
import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from queue import Queue, Empty

from GUI.Frames.PlayAction.PlayersFrame import PlayersFrame
from GUI.Frames.PlayAction.ActionsFrame import ActionsFrame
from GUI.Frames.PlayAction.TimeFrame import TimeFrame

from GUI.Custom.LabeledEntry import LabeledEntry
from Logging.logger import network_message, game_message
from Networking.UDPServerThread import UDPServerThread


class PlayActionScene(ttk.Frame):
    def __init__(self, container, database):
        super().__init__(container)
        

        self.game = container
        self.db = database
        self.queue = Queue()

        # if self.game.addr_from == "127.0.0.1":
        self.game.server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.game.server_socket.bind(("127.0.0.1", 7501))
        network_message("UDP server is up and listening!")

        self.server_thread = UDPServerThread(self.game.server_socket, self.queue)
        self.server_thread.start()
        self.game.client_socket.sendto("202".encode(), self.game.send_to_location)
        self.check_queue()

        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)

        # self.grid_columnconfigure(0, weight=1)

        self.players_frame = PlayersFrame(self, self.game)
        self.players_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.actions_frame = ActionsFrame(self, self.game)
        self.actions_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.time_frame = TimeFrame(self, self.game)
        self.time_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.grid(row=0, column=0, sticky="n")


    def check_queue(self):
        try:
            while True:
                transmission_received = self.queue.get_nowait()
                code = transmission_received[0]
                addr_from = transmission_received[1][0]
                port_from = transmission_received[1][1]

                network_message(f"Code {code} from {addr_from}:{port_from}")

                self.handle_event(code)

                self.queue.task_done()
        except Empty:
            pass

        self.after(5, self.check_queue)

    
    def handle_event(self, code):
        if ":" in code:
            player_transmitting = code.split(":")[0]
            player_hit = code.split(":")[1]

            game_message(f"{self.db.get_player_name_from_id(int(player_transmitting))} hit {self.db.get_player_name_from_id(int(player_hit))}!")

            if int(player_transmitting) % 2 == int(player_hit) % 2:
                self.game.broadcast(player_transmitting)

            self.game.broadcast(player_hit)
