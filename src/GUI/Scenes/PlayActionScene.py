import socket
import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from queue import Queue, Empty

from GUI.Custom.LabeledEntry import LabeledEntry
from Logging.logger import general_message, network_message
from Networking.UDPServerThread import UDPServerThread


class PlayActionScene(ttk.Frame):
    def __init__(self, container, database):
        super().__init__(container)

        self.game = container
        self.db = database
        self.queue = Queue()

        if self.game.addr_from == "127.0.0.1":
            self.server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.server_socket.bind(("0.0.0.0", 7501))
            network_message("UDP server is up and listening!")

            self.server_thread = UDPServerThread(self.server_socket, self.queue)
            self.server_thread.start()
            self.check_queue()

        ttk.Label(self, text="PlayActionScene").grid(row=0, column=0)

        self.grid()


    def check_queue(self):
        try:
            while True:
                transmission_received = self.queue.get_nowait()
                code = int(transmission_received[0])
                addr_from = transmission_received[1][0]
                port_from = transmission_received[1][1]

                network_message(f"Code {code} from {addr_from}:{port_from}")

                if code == 202:
                    self.game_started = True
                    network_message("Network Game Start!")

                self.queue.task_done()
        except Empty:
            pass

        self.after(5, self.check_queue)