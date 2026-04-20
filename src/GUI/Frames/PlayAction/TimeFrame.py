import tkinter as tk
import ttkbootstrap as ttk

from Logging.logger import network_message

class TimeFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container, relief="raised", borderwidth=2)

        self.game = main_game
        self.scene = container

        self.time_remaining_seconds = 360

        if self.game.debug_flags["Debug"]:
            self.time_remaining_seconds = 15

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.time_label = None

        self.update_time_label()
        self.after(1000, self.timer)

    
    def timer(self): 

        if self.time_remaining_seconds == 0:
            self.game.end_game()

            self.time_label.destroy()
            self.time_label = ttk.Label(self, text=f"GAME OVER!", anchor="center")
            self.time_label.grid(row=0, column=0, sticky="nsew")

            self.game.server_socket.close()
            network_message("UDP Server is closed!")

            self.scene.show_button()

        else:
            self.time_remaining_seconds -= 1
            self.update_time_label()

        if self.scene.game_running:
            self.after(1000, self.timer)


    def update_time_label(self):
        min = str(self.time_remaining_seconds // 60)
        sec = "00" if self.time_remaining_seconds % 60 == 0 else str(self.time_remaining_seconds % 60)

        if self.time_label is not None:
            self.time_label.destroy()

        self.time_label = ttk.Label(self, text=f"Time Remaining: {min}:{sec}", anchor="center")
        self.time_label.grid(row=0, column=0, sticky="nsew")
