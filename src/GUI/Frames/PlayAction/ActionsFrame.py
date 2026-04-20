import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame


class ActionsFrame(ttk.Frame):
    def __init__(self, container, main_game):
        super().__init__(container, relief="raised", borderwidth=2)

        self.game = main_game
        self.scene = container

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.messages = []

        ttk.Label(self, text="Current Actions", anchor="center").grid(row=0, column=0, sticky="nsew", pady=(10, 8))

        self.scrolling_frame = ScrolledFrame(self, autohide=True)
        self.scrolling_frame.grid(row=1, column=0, sticky="nsew")

    def add_event(self, message: str):
        self.messages.insert(0, message)

    def update_scroll_frame(self):
        for label in self.scrolling_frame.winfo_children():
            label.destroy()
        
        for message in self.messages:
            ttk.Label(self.scrolling_frame, text=message).pack()




