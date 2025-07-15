import tkinter as tk
import logging
from tkinter import messagebox
from datetime import datetime

from .ChangeMoodDialog import ChangeMoodDialog
from .FindTextDialog import FindTextDialog

from ds.UndoRedoStack import UndoRedoStack
from db.DatabaseManager import DatabaseManager

class EditorWindow(tk.Toplevel):
    def __init__(self, master, entry_id=None, content="", mood="", date=''):
        super().__init__(master)
        self.title("Edit entries")
        self.geometry("600x400")

        self.db = DatabaseManager()
        self.undo_stack = UndoRedoStack()
        self.redo_stack = UndoRedoStack()

        self.entry_id = entry_id
        self.mood = mood
        self.date = date

        self.last_saved_text = content
        self.last_saved_mood = mood

        self.text = tk.Text(self, wrap="word")
        self.text.insert("1.0", content)
        self.text.pack(expand=True, fill="both", padx=10, pady=10)

        self.last_text = self.text.get("1.0", "end-1c")

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Save to DB (Ctrl+S)", command=self.save_to_db)
        file_menu.add_command(label="Delete from DB and exit", command=self.delete_entry)
        file_menu.add_separator()
        file_menu.add_command(label="Close Window (Ctrl+W)", command=self.close_window)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=self.undo)
        edit_menu.add_command(label="Redo (Ctrl+Y)", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Edit entry mood", command=self.edit_mood)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find (Ctrl+F)", command=self.find_text)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind("<Control-s>", self.save_to_db)
        self.bind("<Control-f>", self.find_text)
        self.bind("<Control-w>", self.close_window)
        self.text.bind("<<Modified>>", self.on_text_change)

        self.focus_set()

    def close_window(self, event=None):
        content = self.text.get("1.0", "end-1c").strip()
        mood = self.mood
        if self.last_saved_text != content or self.last_saved_mood != mood:
            if not messagebox.askyesno("Exit", "Are you sure you want to exit the editor?\nUnsaved changes will be lost!"):
                return
        self.destroy()
        logging.info("Editor window closed.")
        if hasattr(self.master, 'refresh_entries'):
            self.master.refresh_entries()

    def on_text_change(self, event=None):
        current_text = self.text.get("1.0", "end-1c")
        if current_text != self.last_text:
            self.undo_stack.push(self.last_text)
            self.last_text = current_text
            self.redo_stack.clear()
        self.text.edit_modified(False)

    def undo(self, event=None):
        if self.undo_stack.is_empty():
            return
        self.redo_stack.push(self.text.get("1.0", "end-1c"))
        self.set_text(self.undo_stack.pop())
        logging.info("Undo performed.")

    def redo(self, event=None):
        if self.redo_stack.is_empty():
            return
        self.undo_stack.push(self.text.get("1.0", "end-1c"))
        self.set_text(self.redo_stack.pop())
        logging.info("Redo performed.")

    def set_text(self, content):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
        self.last_text = content
        self.text.edit_modified(False)

    def find_text(self, event=None):
        FindTextDialog(self)

    def edit_mood(self, event=None):
        dialog = ChangeMoodDialog(self, self.mood)
        if dialog.result is not None:
            self.mood = dialog.result

    def save_to_db(self, event=None):
        content = self.text.get("1.0", "end-1c").strip()

        if self.mood == '':
            mood = 'No mood set'
        else:
            mood = self.mood

        if not content:
            self.attributes("-disabled", True)
            messagebox.showwarning("Empty", "Editor is empty. Nothing to save.")
            self.attributes("-disabled", False)
            return
        if self.entry_id is None:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.insert_entry(current_date, content, mood)

            entry_id = self.db.fetch_entry_id(date=current_date, content=content)[0]
            if entry_id:
                self.entry_id = entry_id
            entry_info = self.db.fetch_entry_info(entry_id=entry_id)
            if entry_info:
                self.date = entry_info[0]
                self.mood = entry_info[1]

        else:
            self.db.update_entry(self.entry_id, content, mood)
        logging.info(f"{'Created new entry' if self.entry_id is None else f'Updated entry ID {self.entry_id}'} in DB.")

        self.last_saved_text = content
        self.last_saved_mood = mood

        if hasattr(self.master, 'refresh_entries'):
            self.master.refresh_entries()

        self.attributes("-disabled", True)
        messagebox.showinfo("Saved", "Entry saved to database.")
        self.attributes("-disabled", False)
        self.focus_set()

    def delete_entry(self):
        if self.entry_id is None:
            self.attributes("-disabled", True)
            messagebox.showerror("Delete", "No record to delete")
            self.attributes("-disabled", False)

            self.focus_set()
        else:
            if messagebox.askyesno("Delete", "Are you sure you want to delete this entry?"):

                self.db.delete_entry(self.entry_id)

                logging.info(f"Deleted entry with ID {self.entry_id}.")
                self.attributes("-disabled", True)
                messagebox.showinfo("Deleted", "Entry deleted.")
                self.attributes("-disabled", False)

                self.last_saved_text = self.text.get("1.0", "end-1c").strip()
                self.last_saved_mood = self.mood

                self.close_window()
            else:
                self.focus_set()