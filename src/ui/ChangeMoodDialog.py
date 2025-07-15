import tkinter as tk
from tkinter import simpledialog

class ChangeMoodDialog(simpledialog.Dialog):
    def __init__(self, parent, initial_text):
        self.initial_text = initial_text
        super().__init__(parent)

    def body(self, master):
        tk.Label(master, text="Change mood:").pack(pady=5)
        self.entry = tk.Entry(master, width=40)
        self.entry.pack(padx=10, pady=5)
        self.title = "Mood"
        self.entry.insert(0, self.initial_text)  # Set initial text
        return self.entry

    def apply(self):
        self.result = self.entry.get()