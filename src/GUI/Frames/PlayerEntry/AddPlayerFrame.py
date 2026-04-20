import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.dialogs import Querybox

from GUI.Custom.LabeledEntry import LabeledEntry
from Logging.logger import debug_message


class AddPlayerFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container)

        self.game = main_game
        self.scene = container

        self.add_player_id = tk.StringVar()
        self.add_player_equip_id = tk.StringVar()

        # Add Player
        self.add_player_label = ttk.Label(self, text="Add a Player")
        self.add_player_label.grid(row=0, column=0, padx=2, pady=2, columnspan=3)

        self.enter_id_entry = LabeledEntry(self, label="Enter ID:", textvariable=self.add_player_id, width=7)
        self.enter_id_entry.grid(row=1, column=0, padx=2, pady=2)

        self.enter_equipment_entry = LabeledEntry(self, label="Enter Equipment ID:", textvariable=self.add_player_equip_id)
        self.enter_equipment_entry.grid(row=1, column=1, padx=2, pady=2)

        self.add_player_button = ttk.Button(self, text="Add", command=self.add_player)
        self.add_player_button.grid(row=1, column=2, padx=2, pady=2)



    def add_player(self):
        id = self.add_player_id.get()
        equip_id = self.add_player_equip_id.get()
        name = ""

        if id == "Enter ID:":
            debug_message("Player ID field empty!")
            Messagebox.ok("Please enter a player ID!", "Error!")

            return
        
        if equip_id == "Enter Equipment ID:":
            debug_message("Equipment ID field empty!")
            Messagebox.ok("Please enter an equipment ID!", "Error!")

            return
        
        if not id.isdecimal():
            debug_message("ID is not a decimal")
            Messagebox.ok("Please enter a number in ID box", "Error!")

            return

        if not equip_id.isdecimal():
            debug_message("Equipment ID is not a decimal")
            Messagebox.ok("Please enter a number in Equipment ID box", "Error!")

            return
        

        id = int(id)
        equip_id = int(equip_id)

        # Check for max team size (n <= 15)
        if equip_id % 2 == 1:
            # Red Team
            if len(self.game.red_team) >= 15:
                debug_message("Red Team is Full!")
                Messagebox.ok("Red Team is Full!", "Error!")
                return
        else:
            # Green Team
            if len(self.game.green_team) >= 15:
                debug_message("Green Team is Full!")
                Messagebox.ok("Green Team is Full!", "Error!")
                return


        # Checks if ID is in Database
        if not self.game.db.does_player_exist_from_id(id):
            name = Querybox.get_string("Enter a name for the new player!")

            if not self.game.db.add_player(id, name):
                Messagebox.ok(self.db.get_error_message(), "Error!")
                

        # Swapping Even/Odd Colors According to Feedback from Sprint 2
        # Add player to respective team
        if equip_id % 2 == 1:
            self.game.red_team[id] = equip_id
        else:
            self.game.green_team[id] = equip_id

        self.game.points[id] = 0      
        self.game.base[id] = False  
    
        self.scene.update_list()
        
        # Network Broadcast
        self.game.broadcast(str(equip_id))
        
        self.add_player_id.set("Enter ID:")
        self.add_player_equip_id.set("Enter Equipment ID:")

        self.scene.focus_set()