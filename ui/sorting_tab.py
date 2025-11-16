import tkinter as tk
from tkinter import ttk
import random

class SortingTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        control_frame = tk.Frame(self.frame)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(control_frame, text="Array Size (max 30)").pack(pady=5)
        self.size_var = tk.IntVar(value=10)
        self.size_spinbox = tk.Spinbox(control_frame, from_=2, to=30, textvariable=self.size_var)
        self.size_spinbox.pack(pady=5)

        tk.Label(control_frame, text="Algorithm Speed (ms)").pack(pady=5)
        self.speed_var = tk.IntVar(value=100)
        self.speed_scale = tk.Scale(control_frame, from_=10, to=1000, orient="horizontal", variable=self.speed_var)
        self.speed_scale.pack(pady=5)

        tk.Button(control_frame, text="Generate Array", command=self.generate_array).pack(pady=5)
        tk.Button(control_frame, text="Bubble Sort", command=self.run_bubble_sort).pack(pady=5)

        self.canvas = tk.Canvas(self.frame, width=700, height=400, bg="white")
        self.canvas.pack(side="left", padx=10, pady=10)

        self.data = []

    def generate_array(self):
        size = self.size_var.get()
        self.data = [random.randint(10, 390) for _ in range(size)]
        self.draw_array()

    def draw_array(self, highlight=None):
        self.canvas.delete("all")
        if not self.data:
            return
        c_width = int(self.canvas["width"])
        c_height = int(self.canvas["height"])
        bar_width = c_width / len(self.data)

        for i, height in enumerate(self.data):
            x0 = i * bar_width
            y0 = c_height - height
            x1 = (i + 1) * bar_width
            y1 = c_height
            color = "red" if highlight and i in highlight else "turquoise"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def run_bubble_sort(self):
        self.bubble_sort_step(0, 0)

    def bubble_sort_step(self, i, j):
        n = len(self.data)
        if i >= n - 1:
            return 

        if j < n - i - 1:
            self.draw_array(highlight=[j, j+1])

            if self.data[j] > self.data[j+1]:
                self.data[j], self.data[j+1] = self.data[j+1], self.data[j]
            self.canvas.after(self.speed_var.get(), lambda: self.bubble_sort_step(i, j+1))
        else:
            self.canvas.after(self.speed_var.get(), lambda: self.bubble_sort_step(i+1, 0))
