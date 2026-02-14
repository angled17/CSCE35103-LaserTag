import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *

class LabeledEntry(ttk.Entry):
    def __init__(self, master=None, label="Default Text", **kwargs):
        super().__init__(master, **kwargs)
        self.label = label
        self.on_exit()

        self.bind('<FocusIn>', self.on_entry)
        self.bind('<FocusOut>', self.on_exit)


    def on_entry(self, event=None):
        if self.get() == self.label:
            self.delete(0, tk.END)

    def on_exit(self, event=None):
        if not self.get():
            self.insert(0, self.label)