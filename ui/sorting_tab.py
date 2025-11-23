import tkinter as tk
from tkinter import ttk
from algorithms.sorting.bubble_sort import bubble_sort
from algorithms.sorting.insertion_sort import insertion_sort
from algorithms.sorting.merge_sort import merge_sort
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
        self.speed_scale = tk.Scale(control_frame, from_=1, to=1000, orient="horizontal", variable=self.speed_var)
        self.speed_scale.pack(pady=5)

        tk.Button(control_frame, text="Generate Array", command=self.generate_array).pack(pady=5)
        tk.Button(control_frame, text="Bubble Sort", command=self.run_bubble_sort).pack(pady=5)
        tk.Button(control_frame, text="Insertion Sort", command=self.run_insertion_sort).pack(pady=5)
        tk.Button(control_frame, text="Merge Sort", command=self.run_merge_sort).pack(pady=5)

        self.canvas = tk.Canvas(self.frame, width=700, height=400, bg="white")
        self.info_frame = tk.Frame(self.frame)
        self.description_label = tk.Label(
            self.info_frame,
            text="Description:",
            font=("Arial", 10, "bold"),
            anchor="center",
            justify="center"
        )
        self.description = tk.Label(
        self.info_frame,
            text="Click on a Sorting Algorithm to view its description.",
            wraplength=250,
            justify="left"
        )
        self.algorithm_descriptions = {
            "bubble": "Bubble Sort repeatedly swaps adjacent elements if they are in the wrong order until the list is sorted.",
            "insertion": "Insertion Sort builds a sorted array one element at a time by inserting elements in their correct position.",
            "merge": "Merge Sort recursively splits the array into halves, sorts each half, and merges them back together."
        }

        self.code_label = tk.Label(
            self.info_frame,
            text="Pseudocode:",
            font=("Arial", 10, "bold"),
            anchor="center",
            justify="center"
        )

        self.code_text = tk.Text(
            self.info_frame,
            height=20,
            width=50,           
            wrap="none",
            font=("Courier", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            borderwidth=1,
            relief="solid"
        )
        self.description_label.pack(pady=(5,0), fill="x")
        self.description.pack(pady=5, fill ="x")
        self.code_label.pack(pady=(5, 0), fill="x")
        self.code_text.pack(pady=5, fill="both", expand=False)
        self.canvas.pack(side="left", padx=10, pady=10)
        self.info_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.data = []
        self.sort_gen = None

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
        if not self.data:
            return
        self.description.config(text=self.algorithm_descriptions["bubble"])
        self.sort_gen = bubble_sort(self.data)
        self.animate_sort_step()    

    def run_insertion_sort(self):
        if not self.data:
            return
        self.description.config(text=self.algorithm_descriptions["insertion"])
        self.sort_gen = insertion_sort(self.data)
        self.animate_sort_step()

    def run_merge_sort(self):
        if not self.data:
            return
        self.description.config(text=self.algorithm_descriptions["merge"])
        self.sort_gen = merge_sort(self.data)
        self.animate_sort_step()

    def animate_sort_step(self):
        try:
            arr, highlight = next(self.sort_gen)
            self.data = arr
            self.draw_array(highlight=highlight)
            self.canvas.after(self.speed_var.get(), self.animate_sort_step)
        except StopIteration:
            return