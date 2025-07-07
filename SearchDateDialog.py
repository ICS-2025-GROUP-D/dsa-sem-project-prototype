import tkinter as tk
import logging
from tkinter import messagebox

from ds.DateBST import DateBST
from db.DatabaseManager import DatabaseManager

class SearchDateDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Search by Date")
        self.transient(master)

        self.db = DatabaseManager()

        tk.Label(self, text="Enter Date (YYYY-MM-DD):").pack(padx=10, pady=5)
        self.entry = tk.Entry(self, width=30)
        self.entry.pack(padx=10, pady=5)
        tk.Button(self, text="Search", command=self.on_search).pack(pady=5)
        tk.Button(self, text="Close", command=self.on_close).pack(pady=5)

    def on_search(self):
        date_query = self.entry.get().strip()
        if not date_query:
            self.attributes("-disabled", True)
            messagebox.showwarning("Input Error", "Please enter a date string.")
            self.attributes("-disabled", False)
            return

        if len(date_query) != 10 or not all(x.isdigit() for x in date_query.split('-')) or date_query[4] != '-' or \
                date_query[7] != '-':
            self.attributes("-disabled", True)
            messagebox.showwarning("Invalid Date Format", "Please enter a valid date in the format YYYY-MM-DD.")
            self.attributes("-disabled", False)
            return
        matching_entries = self.db.search_entries_by_date(date_query)

        if not matching_entries:
            logging.info(f"Filtered entries on {date_query}. Found 0 entries.")
            self.attributes("-disabled", True)
            messagebox.showinfo("Not Found", f"No entries found for date: {date_query}")
            self.attributes("-disabled", False)
            return

        for item in self.master.tree.get_children():
            self.master.tree.delete(item)

        for entry_id, date in matching_entries:
            self.master.tree.insert("", "end", values=(entry_id, date))
        logging.info(f"Filtered entries on {date_query}. Found {len(matching_entries)} entries.")

    def on_close(self):
        self.master.refresh_tree()
        self.destroy()
        logging.info(f"Date search dialog closed.")




