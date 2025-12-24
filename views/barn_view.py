import tkinter as tk
import threading
import time

class BarnWindow:   
    def __init__(self, parent, storage):
        self.top = tk.Toplevel(parent)
        self.top.title("Амбар")
        self.top.geometry("500x800")

        self.storage = storage     

        self.label = tk.Label(self.top, text="Амбар пуст", font=("Arial", 14))
        self.label.pack(pady=20)

        self.refresh()

    def refresh(self):
        if not self.top.winfo_exists():
            return
        if not self.storage:
            self.label.config(text="Амбар пуст")
        else:
            text = "\n".join([f"{k}: {v}" for k, v in self.storage.items()])
            self.label.config(text=text)