import socket
import threading
import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from queue import Queue, Empty

from gui.LabeledEntry import LabeledEntry
from log.logger import general_message, network_message
from networking.UDPServerThread import UDPServerThread


class GameActionFrame(ttk.Frame):
    def __init__(self, container, database):
        super().__init__(container)

        self.game = container
        self.db = database

        ttk.Label(self, text="GameActionFrame").grid(row=0, column=0)

        self.pack()