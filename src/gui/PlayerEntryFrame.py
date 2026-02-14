import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from gui.LabeledEntry import LabeledEntry
from log.logger import general_message


class PlayerEntryFrame(ttk.Frame):
    def __init__(self, container, database):
        super().__init__(container)

        self.game = container
        self.db = database
        self.add_player_id = tk.StringVar()
        self.add_player_name = tk.StringVar()
        self.add_player_equip_id = tk.StringVar()

        self.start_list_row = 6

        self.widgets = []
        self.red_team_labels = []
        self.green_team_labels = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Add Player
        add_player_label = ttk.Label(self, text="Add a Player:")
        add_player_label.grid(row=0, column=0, pady=2, columnspan=4)
        self.widgets.append(add_player_label)

        enter_id_entry = LabeledEntry(self, label="Enter ID:", textvariable=self.add_player_id)
        enter_id_entry.grid(row=1, column=0, pady=2, columnspan=4)
        self.widgets.append(enter_id_entry)   

        enter_name_entry = LabeledEntry(self, label="Enter Name:", textvariable=self.add_player_name)
        enter_name_entry.grid(row=2, column=0, pady=2, columnspan=4)
        self.widgets.append(enter_name_entry)

        enter_equipment_entry = LabeledEntry(self, label="Enter Equipment ID:", textvariable=self.add_player_equip_id)
        enter_equipment_entry.grid(row=3, column=0, pady=2, columnspan=4)
        self.widgets.append(enter_equipment_entry)

        add_player_button = ttk.Button(self, text="Add Player", command=self.add_player)
        add_player_button.grid(row=4, column=0, pady=2, columnspan=4)
        self.widgets.append(add_player_button)

        # Red Team - Left
        red_team_label = ttk.Label(self, text="Red Team")
        red_team_label.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")
        self.widgets.append(red_team_label)

        # Green Team - Right
        green_team_label = ttk.Label(self, text="Green Team")
        green_team_label.grid(row=5, column=2, padx=10, pady=10, columnspan=2, sticky="nsew")
        self.widgets.append(green_team_label)

        self.pack()

    
    def add_player(self):
        id = self.add_player_id.get()
        name = self.add_player_name.get()
        equip_id = self.add_player_equip_id.get()

        if id == "Enter ID:" or name == "Enter Name:" or equip_id == "Enter Equipment ID:":
            general_message("Some player fields are unchanged.")
            Messagebox.ok("Please fill out all three fields!", "Error!")

            return
        
        if not id.isdecimal():
            general_message("ID is not a decimal")
            Messagebox.ok("Please enter a number in ID box", "Error!")

            return
        
        if not name.isalnum():
            general_message("Name is not a alphanumeric")
            Messagebox.ok("Please enter an alphanumeric name in Name box", "Error!")

            return
        
        if not equip_id.isdecimal():
            general_message("Equipment ID is not a decimal")
            Messagebox.ok("Please enter a number in Equipment ID box", "Error!")

            return

        id = int(id)
        equip_id = int(equip_id)

        if self.db.add_player(id, name):
            if equip_id % 2 == 0:
                self.game.red_team[id] = equip_id
                self.red_team_labels.append(ttk.Label(self, text=f"{id} | {name} | {equip_id}"))
            else:
                self.game.green_team[id] = equip_id
                self.green_team_labels.append(ttk.Label(self, text=f"{id} | {name} | {equip_id}"))
            
            self.update_player_list()
        else:
            Messagebox.ok(self.db.get_error_message(), "Error!")

    
    def update_player_list(self):
        # Update Red
        red_index = self.start_list_row
        green_index = self.start_list_row

        for red_player in self.red_team_labels:
            red_player.grid(row=red_index, column=1)
            red_index += 1

        for green_player in self.green_team_labels:
            green_player.grid(row=green_index, column=3)
            green_index += 1
