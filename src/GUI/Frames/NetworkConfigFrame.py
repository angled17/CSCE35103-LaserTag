import tkinter as tk
import ttkbootstrap as ttk

class NetworkConfigFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container)

        self.game = main_game

        self.paddingx = 2
        self.paddingy = 2
        
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

        self.network_addr = tk.StringVar()
        self.network_addr.set(f"{self.game.addr_from}:{self.game.addr_from_port}")

        self.network_label = ttk.Label(self, text="Network Address")
        self.network_label.grid(row=0, column=0, pady=2, columnspan=2)

        self.network_entry = ttk.Entry(self, textvariable=self.network_addr, width=21)
        self.network_entry.grid(row=1, column=0, padx=self.paddingx, pady=self.paddingy)

        self.update_address_button = ttk.Button(self, text="Update", command=self.update_network)
        self.update_address_button.grid(row=1, column=1, padx=self.paddingx, pady=self.paddingy)

    
    def update_network(self):
        addr = self.network_addr.get().split(":")

        self.game.addr_from = addr[0]
        self.game.addr_from_port = int(addr[1])

        self.game.send_to_location = (addr[0], int(addr[1]))


    
