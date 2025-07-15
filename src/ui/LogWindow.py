import logging
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.yview(tk.END)
        self.text_widget.after(0, append)

class LogWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Application Log")
        self.geometry("600x300")

        self.text_area = ScrolledText(self, state='disabled', wrap='word')
        self.text_area.pack(expand=True, fill='both')

        text_handler = TextHandler(self.text_area)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
        text_handler.setFormatter(formatter)
        logging.getLogger().addHandler(text_handler)