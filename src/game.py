import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *

from log.logger import general_message

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        
        # Root Window Config
        self.title("Laser Tag!")
        self.geometry('700x700')
        self.resizable(False, False)
        
        # Game Information {id: equip_id}
        self.red_team = {}
        self.green_team = {}