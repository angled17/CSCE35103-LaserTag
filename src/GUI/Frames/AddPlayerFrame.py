import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

from GUI.Custom.LabeledEntry import LabeledEntry
from Logging.logger import general_message, network_message


class AddPlayerFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container, relief="raised", borderwidth=2)

        self.game = main_game

        self.add_player_id = tk.StringVar()
        self.add_player_name = tk.StringVar()
        self.add_player_equip_id = tk.StringVar()

        # Add Player
        self.add_player_label = ttk.Label(self, text="Add a Player")
        self.add_player_label.grid(row=0, column=0, padx=2, pady=2, columnspan=3)

        self.enter_id_entry = LabeledEntry(self, label="Enter ID:", textvariable=self.add_player_id, width=7)
        self.enter_id_entry.grid(row=1, column=0, padx=2, pady=2)

        # enter_name_entry = LabeledEntry(self, label="Enter Name:", textvariable=self.add_player_name)
        # enter_name_entry.grid(row=self.start_list_row - 5, column=0, pady=2, columnspan=4)
        # self.entries.append(enter_name_entry)

        self.enter_equipment_entry = LabeledEntry(self, label="Enter Equipment ID:", textvariable=self.add_player_equip_id)
        self.enter_equipment_entry.grid(row=1, column=1, padx=2, pady=2)

        self.add_player_button = ttk.Button(self, text="Add", command=self.add_player)
        self.add_player_button.grid(row=1, column=2, padx=2, pady=2)



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
        network_message(f"Broadcasted {equip_id} to {self.game.send_to_location[0]}:{self.game.send_to_location[1]}")

        id = int(id)
        equip_id = int(equip_id)

        # Swapping Even/Odd Colors According to Feedback from Sprint 2
        if self.db.add_player(id, name):
            if equip_id % 2 == 1:
                self.game.red_team[id] = equip_id
            else:
                self.game.green_team[id] = equip_id
            
            for entry in self.entries:
                entry.on_update()
        
            self.update_player_list()
        else:
            Messagebox.ok(self.db.get_error_message(), "Error!")