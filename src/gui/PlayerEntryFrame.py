import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from gui.LabeledEntry import LabeledEntry
from log.logger import general_message, network_message


class PlayerEntryFrame(ttk.Frame):
    def __init__(self, container, database, socket):
        super().__init__(container)

        self.game = container
        self.db = database
        self.socket = socket

        self.add_player_id = tk.StringVar()
        self.add_player_name = tk.StringVar()
        self.add_player_equip_id = tk.StringVar()

        self.start_list_row = 7

        self.entries = []
        self.player_labels = []

        self.bind("<Key>", self.game_start)
        self.focus_set()

        # Add Player
        add_player_label = ttk.Label(self, text="Add a Player:")
        add_player_label.grid(row=0, column=0, pady=2, columnspan=4)

        enter_id_entry = LabeledEntry(self, label="Enter ID:", textvariable=self.add_player_id)
        enter_id_entry.grid(row=1, column=0, pady=2, columnspan=4)
        self.entries.append(enter_id_entry)   

        enter_name_entry = LabeledEntry(self, label="Enter Name:", textvariable=self.add_player_name)
        enter_name_entry.grid(row=2, column=0, pady=2, columnspan=4)
        self.entries.append(enter_name_entry)

        enter_equipment_entry = LabeledEntry(self, label="Enter Equipment ID:", textvariable=self.add_player_equip_id)
        enter_equipment_entry.grid(row=3, column=0, pady=2, columnspan=4)
        self.entries.append(enter_equipment_entry)

        add_player_button = ttk.Button(self, text="Add Player", command=self.add_player)
        add_player_button.grid(row=4, column=0, pady=2, columnspan=4)

        players_label = ttk.Label(self, text="Players")
        players_label.grid(row=5, column=0, columnspan=4)

        # Red Team - Left
        red_team_label = ttk.Label(self, text="Red Team")
        red_team_label.grid(row=self.start_list_row - 1, column=0, padx=10, pady=10, columnspan=2)

        # Green Team - Right
        green_team_label = ttk.Label(self, text="Green Team")
        green_team_label.grid(row=self.start_list_row - 1, column=2, padx=10, pady=10, columnspan=2)

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

        self.socket.sendto(equip_id.encode(), self.game.send_to_location)
        network_message(f"Broadcasted {equip_id} to {self.game.send_to_location[0]:{self.game.send_to_location[1]}}")

        id = int(id)
        equip_id = int(equip_id)

        if self.db.add_player(id, name):
            if equip_id % 2 == 0:
                self.game.red_team[id] = equip_id
            else:
                self.game.green_team[id] = equip_id
            
            for entry in self.entries:
                entry.on_update()
        
            self.update_player_list()
        else:
            Messagebox.ok(self.db.get_error_message(), "Error!")

    
    def update_player_list(self):
        # Destory Player Labels
        for l in self.player_labels:
            l.destroy()

        # Update Red
        red_index = self.start_list_row
        green_index = self.start_list_row

        for red_player_id in self.game.red_team:
            t_lab = ttk.Label(self, text=f"{red_player_id} | {self.db.get_player_from_id(red_player_id)} | {self.game.red_team[red_player_id]}")
            t_lab.grid(row=red_index, column=1, padx=5)
            self.player_labels.append(t_lab)

            red_index += 1

        for green_player_id in self.game.green_team:
            t_lab = ttk.Label(self, text=f"{green_player_id} | {self.db.get_player_from_id(green_player_id)} | {self.game.green_team[green_player_id]}")
            t_lab.grid(row=green_index, column=3, padx=5)
            self.player_labels.append(t_lab)

            green_index += 1


    def game_start(self, event):
        if event.keysym == "F5":
            self.socket.sendto("202".encode(), self.game.send_to_location)
            self.game.start_game()
