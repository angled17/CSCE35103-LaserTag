import socket
import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from queue import Queue, Empty

from gui.SplashFrame import SplashFrame
from gui.PlayerEntryFrame import PlayerEntryFrame
from gui.GameActionFrame import GameActionFrame

from log.logger import general_message, network_message

from networking.UDPServerThread import UDPServerThread

class App(ttk.Window):
    def __init__(self, d):
        super().__init__(themename="darkly")
        
        # Root Window Config
        self.title("Laser Tag!")
        self.geometry('700x700')
        # self.resizable(False, False)

        self.db = d
        self.queue = Queue()
        self.game_started = False

        # UDP Config
        self.addr_from = "127.0.0.1"
        self.addr_from_port = 7501

        self.send_to_location = (self.addr_from, self.addr_from_port)

        self.server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.server_socket.bind(("0.0.0.0", 7501))
        network_message("UDP server is up and listening!")

        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client_socket.bind((self.addr_from, 7500))
        network_message("UDP client is up!")

        self.server_thread = UDPServerThread(self.server_socket, self.queue)
        self.server_thread.start()
        self.check_queue()
        
        # Game Information {id: equip_id}
        self.red_team = {}
        self.green_team = {}

        self.splash_screen_frame = SplashFrame(self)
        self.player_entry_frame = None
        self.game_action_frame = None


    def start_game(self):
        self.game_action_frame = GameActionFrame(self, self.db)
        self.player_entry_frame.destroy()


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