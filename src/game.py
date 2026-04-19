import socket
import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from pygame import mixer

from GUI.Scenes.SplashScene import SplashScene
from GUI.Scenes.PlayerEntryScene import PlayerEntryScene
from GUI.Scenes.PlayActionScene import PlayActionScene

from Logging.logger import network_message, music_message

from Networking.UDPServerThread import UDPServerThread


class App(ttk.Window):
    def __init__(self, d, flags):
        # Images
        self.logo_image = Image.open('static/logo.jpg')

        mixer.init(channels=2)

        self.sfx_channel = mixer.Channel(0)
        self.music_channel = mixer.Channel(1)

        self.music_track_sounds = {
            "Track01": mixer.Sound("static/tracks/Track01.ogg"),
            "Track02": mixer.Sound("static/tracks/Track02.ogg"),
            "Track03": mixer.Sound("static/tracks/Track03.ogg"),
            "Track04": mixer.Sound("static/tracks/Track04.ogg"),
            "Track05": mixer.Sound("static/tracks/Track05.ogg"),
            "Track06": mixer.Sound("static/tracks/Track06.ogg"),
            "Track07": mixer.Sound("static/tracks/Track07.ogg"),
            "Track08": mixer.Sound("static/tracks/Track08.ogg")
        }

        music_message("Tracks Loaded!")

        self.music_delay = 9

        super().__init__(themename="darkly")
        
        self.splash_image = ImageTk.PhotoImage(self.logo_image.resize((self.winfo_width(), self.winfo_height())), Image.Resampling.LANCZOS)
        
        # Root Window Config
        self.title("Laser Tag!")
        self.geometry('700x700')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.db = d
        self.game_started = False

        self.debug_flags = flags

        # UDP Config
        self.addr_to = "0.0.0.0"

        # From feedback of Sprint 3
        self.addr_to_port = 7500

        self.send_to_location = (self.addr_to, self.addr_to_port)

        self.server_socket = None
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # self.client_socket.bind(("127.0.0.1", 7500)) <- According to feedback from Sprint 2, do not bind client socket.
        network_message("UDP client is up!")
        

        # Game Information {id: equip_id}
        self.red_team = {}
        self.green_team = {}

        self.points = {}


        self.splash_screen_frame = None
        self.player_entry_frame = None
        self.play_action_frame = None


        list_of_flags = list(self.debug_flags.values())

        if not any(self.debug_flags.values()) or list_of_flags == [True, False, False, False] or list_of_flags == [True, True, False, False]:
            self.splash_screen_frame = SplashScene(self)

        if list_of_flags == [True, False, True, False]:
            self.player_entry_frame = PlayerEntryScene(self, self.db, self.client_socket)

        if list_of_flags == [True, False, False, True]:
            self.play_action_frame = PlayActionScene(self, self.db)

        if list_of_flags == [True, False, False, False]:
            self.red_team = {1: 1, 3: 3}
            self.green_team = {2: 2, 4: 4}


    def start_game(self):
        self.play_action_frame = PlayActionScene(self, self.db)
        self.player_entry_frame.destroy()

    def broadcast(self, msg):
        self.client_socket.sendto(msg.encode(), self.send_to_location)
        network_message(f"Broadcasted {msg} to {self.send_to_location[0]}:{self.send_to_location[1]}")
