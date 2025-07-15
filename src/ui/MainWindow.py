import tkinter as tk
import logging
from tkinter import ttk

from .LogWindow import LogWindow
from .EditorWindow import EditorWindow
from .SearchDateDialog import SearchDateDialog

from ds.MoodHashTable import MoodHashTable
from ds.SearchDateBST import SearchDateBST
from db.DatabaseManager import DatabaseManager

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Journal Application")
        self.geometry("500x400")

        self.log_window = LogWindow(self)

        self.db = DatabaseManager()
        self.mood_hash_table = MoodHashTable()
        self.search_date_bst = SearchDateBST()

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New entry (Ctrl+N)", command=self.open_new_entry)
        file_menu.add_command(label="Search by date (Ctrl+F)", command=self.search_by_date)
        file_menu.add_command(label="Refresh view (F5)", command=self.refresh_entries)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="Options", menu=file_menu)

        filter_frame = ttk.Frame(self)
        filter_frame.pack(pady=5)

        filter_label = ttk.Label(filter_frame, text="Filter by mood:")
        filter_label.pack(side="left", padx=(0, 10))

        self.mood_filter_var = tk.StringVar()
        self.mood_filter = ttk.Combobox(filter_frame, textvariable=self.mood_filter_var, state="readonly")
        self.mood_filter.pack(side="left")

        self.tree = ttk.Treeview(self, columns=("id", "date", "mood"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date created")
        self.tree.heading("mood", text="Mood") # New column for mood
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("date", anchor="center")
        self.tree.column("mood", anchor="center") #New column for mood
        self.tree.pack(expand=True, fill="both", padx=10, pady=5)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.mood_filter.bind("<<ComboboxSelected>>", self.filter_by_mood)

        self.bind("<Control-n>", self.open_new_entry)
        self.bind("<Control-f>", self.search_by_date)
        self.bind("<F5>", self.refresh_entries)

        self.refresh_entries()

        self.focus_set()

    def refresh_entries(self, event=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        results = self.db.fetch_all_entries()

        for entry_id, date, mood in results:
            self.tree.insert("", "end", values=(entry_id, date, mood))

        self.build_search_date_bst()

        mood_set = self.build_mood_hash_table()
        mood_list = (list(mood_set))
        self.mood_filter['values'] = ["All"] + mood_list
        self.mood_filter.set("All")

    def build_mood_hash_table(self):
        results = self.db.fetch_all_entries()
        mood_set = set()
        for entry_id, date, mood in results:
            self.mood_hash_table.add_entry(mood, entry_id)
            logging.info(f"Added mood of entry {entry_id} to hash table")
            mood_set.add(mood)
        return mood_set

    def open_new_entry(self, event=None):
        EditorWindow(self)

    def on_double_click(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        entry_id, date, mood = item["values"]

        row = self.db.fetch_entry(entry_id)

        if row:
            EditorWindow(self, entry_id=entry_id, content=row[0], mood=mood, date=date)
        logging.info(f"Opened entry with ID {entry_id}.")

    def build_search_date_bst(self):
        result = self.db.fetch_all_entries_bst()
        for entry_id, date, mood in result:
            self.search_date_bst.insert(date)
            logging.info(f"Inserted date of entry ID {entry_id} into binary tree.")

    def search_by_date(self, event=None):
        SearchDateDialog(self)

    def filter_by_mood(self, event=None):
        selected_mood = self.mood_filter_var.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        results = self.db.fetch_all_entries()

        if selected_mood == "All":
            for entry_id, date, mood in results:
                self.tree.insert("", "end", values=(entry_id, date, mood))
        else:
            matching_ids = set(self.mood_hash_table.get_entries(selected_mood))
            for entry_id, date, mood in results:
                if entry_id in matching_ids:
                    self.tree.insert("", "end", values=(entry_id, date, mood))