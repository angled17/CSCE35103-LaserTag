import socket
import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *

from GUI.Scenes.SplashScene import SplashScene
from GUI.Scenes.PlayerEntryScene import PlayerEntryScene
from GUI.Scenes.PlayActionScene import PlayActionScene

from Logging.logger import general_message, network_message

from Networking.UDPServerThread import UDPServerThread

class App(ttk.Window):
    def __init__(self, d):
        super().__init__(themename="darkly")
        
        # Root Window Config
        self.title("Laser Tag!")
        self.geometry('700x700')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.resizable(False, False)

        self.db = d
        self.game_started = False

        # UDP Config
        self.addr_from = "127.0.0.1"
        self.addr_from_port = 7501

        self.send_to_location = (self.addr_from, self.addr_from_port)

        self.server_socket = None
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # self.client_socket.bind(("127.0.0.1", 7500)) <- According to feedback from Sprint 2, do not bind client socket.
        network_message("UDP client is up!")
        
        # Game Information {id: equip_id}
        self.red_team = {}
        self.green_team = {}

        self.splash_screen_frame = SplashScene(self)
        self.player_entry_frame = None
        self.play_action_frame = None


    def start_game(self):
        self.play_action_frame = PlayActionScene(self, self.db)
        self.player_entry_frame.destroy()
