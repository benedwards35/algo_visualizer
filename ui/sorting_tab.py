import tkinter as tk
from tkinter import ttk

class SortingTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        tk.Label(self.frame, text="Sorting Tab Loaded").pack(padx=20, pady=20)

        self.canvas = tk.Canvas(self.frame, width=700, height=400, bg="white")
        self.canvas.pack(padx=10, pady=10)
