import tkinter as tk
import ttkbootstrap as ttk


class TimeFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container, relief="raised", borderwidth=2)

        self.game = main_game
        self.scene = container

        self.time_remaining_seconds = 360

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.time_label = None

        self.update_time_label()
        self.after(1000, self.timer)

    
    def timer(self):
        self.time_remaining_seconds -= 1
        self.update_time_label()

        self.after(1000, self.timer)


    def update_time_label(self):
        min = str(self.time_remaining_seconds // 60)
        sec = "00" if self.time_remaining_seconds % 60 == 0 else str(self.time_remaining_seconds % 60)

        if self.time_label is not None:
            self.time_label.destroy()

        self.time_label = ttk.Label(self, text=f"Time Remaining: {min}:{sec}", anchor="center")
        self.time_label.grid(row=0, column=0, sticky="nsew")
