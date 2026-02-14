import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *

from gui.LabeledEntry import LabeledEntry
from log.logger import general_message


class GameActionFrame(ttk.Frame):
    def __init__(self, container, database):
        super().__init__(container)
        
        self.db = database