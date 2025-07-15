import tkinter as tk
import logging
from tkinter import messagebox

from ds.MatchLinkedList import MatchLinkedList
from ds.ReplaceQueue import ReplaceQueue

class FindTextDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Find")
        self.transient(master)
        self.resizable(False, False)
        self.grab_set()

        self.editor = master
        self.match_list = MatchLinkedList()
        self.replace_queue = ReplaceQueue()

        tk.Label(self, text="Find:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_var = tk.StringVar()

        tk.Label(self, text="Replace with:").grid(row=2, column=0, padx=5, pady=5)
        self.replace_entry = tk.Entry(self, width=30)
        self.replace_entry.grid(row=2, column=1, columnspan=4, padx=5, pady=5)

        self.entry_var.trace_add("write", self.on_entry_change)
        self.entry = tk.Entry(self, width=30, textvariable=self.entry_var)
        self.entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        self.entry.focus()

        tk.Button(self, text="Previous", command=self.on_prev).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self, text="Next", command=self.on_next).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self, text="Replace All", command=self.on_replace_all).grid(row=1, column=3, padx=5, pady=5)
        tk.Button(self, text="Close", command=self.on_close).grid(row=1, column=4, padx=5, pady=5)

    def initialize_search(self):
        query = self.entry.get()
        if not query:
            return False

        self.editor.text.tag_remove("highlight", "1.0", "end")
        self.editor.text.tag_remove("current_match", "1.0", "end")
        self.match_list.clear()

        start = "1.0"
        while True:
            pos = self.editor.text.search(query, start, stopindex="end", nocase=False)
            if not pos:
                break
            end_pos = f"{pos}+{len(query)}c"

            self.editor.text.tag_add("highlight", pos, end_pos)
            self.match_list.add(pos)

            start = end_pos
            logging.info(f"Added instance of {query} at position {pos} into Find linked list.")

        self.editor.text.tag_config("highlight", background="yellow", foreground="black")
        self.editor.text.tag_config("current_match", background="orange", foreground="black")
        logging.info(f"Filtered matches on {query}. Found {self.match_list.match_count()} instances.")

        if self.match_list.head is None:
            self.attributes("-disabled", True)
            messagebox.showinfo("Find", f"No matches found for '{query}'")
            self.attributes("-disabled", False)
            return False
        else:
            self.editor.last_search_query = query
            self.highlight_current_match(self.match_list.get_current())

            self.editor.text.see(self.match_list.get_current())
            self.editor.text.mark_set("insert", self.match_list.get_current())
            self.editor.text.focus()
            return True

    def highlight_current_match(self, pos):
        self.editor.text.tag_remove("current_match", "1.0", "end")
        if pos:
            end_pos = f"{pos}+{len(self.editor.last_search_query)}c"
            self.editor.text.tag_add("current_match", pos, end_pos)

    def on_entry_change(self, *args):
        if not self.entry_var.get().strip():
            self.editor.text.tag_remove("highlight", "1.0", "end")
            self.match_list.clear()

    def on_next(self):
        if self.match_list.head is None:
            if not self.initialize_search():
                return
        else:
            pos = self.match_list.go_next()
            if pos:
                self.highlight_current_match(pos)

                self.editor.text.see(pos)
                self.editor.text.mark_set("insert", pos)
                self.editor.text.focus()
            else:
                self.attributes("-disabled", True)
                messagebox.showinfo("Find", "No next match.")
                self.attributes("-disabled", False)

    def on_prev(self):
        if self.match_list.head is None:
            if not self.initialize_search():
                return
        else:
            pos = self.match_list.go_prev()
            if pos:
                self.highlight_current_match(pos)

                self.editor.text.see(pos)
                self.editor.text.mark_set("insert", pos)
                self.editor.text.focus()
            else:
                self.attributes("-disabled", True)
                messagebox.showinfo("Find", "No previous match.")
                self.attributes("-disabled", False)

    def on_replace_all(self):
        query = self.entry_var.get()
        replacement = self.replace_entry.get()

        if not query:
            return

        self.editor.text.tag_remove("highlight", "1.0", "end")
        self.editor.text.tag_remove("current_match", "1.0", "end")

        self.match_list.clear()
        self.replace_queue = ReplaceQueue()

        start = "1.0"
        while True:
            pos = self.editor.text.search(query, start, stopindex="end", nocase=False)
            if not pos:
                break
            end_pos = f"{pos}+{len(query)}c"
            original_text = self.editor.text.get(pos, end_pos)
            self.replace_queue.enqueue(original_text)
            logging.info(f"Enqueued instance of '{original_text}' at {pos} into replace queue.")
            self.editor.text.delete(pos, end_pos)
            self.editor.text.insert(pos, replacement)
            start = f"{pos}+{len(replacement)}c"

        logging.info(f"Replaced all occurrences of '{query}' with '{replacement}'.")
        self.attributes("-disabled", True)
        messagebox.showinfo("Replace All", f"All occurrences of '{query}' replaced with '{replacement}'.")
        self.attributes("-disabled", False)

    def on_close(self):
        self.editor.text.tag_remove("highlight", "1.0", "end")
        self.editor.text.tag_remove("current_match", "1.0", "end")

        self.match_list.clear()
        self.destroy()
        logging.info("Find/replace dialog closed.")
