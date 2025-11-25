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
            height=10,
            width=150,           
            wrap="none",
            font=("Courier", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            borderwidth=1,
            relief="solid"
        )

        self.algorithm_pseudocode = {
    "bubble": """1  n = len(array)
2  arr = array[:]
3  for i in range(n):
4      for j in range(n - i - 1):
5          yield arr, (j, j+1)
6          if arr[j] > arr[j + 1]:
7              arr[j], arr[j + 1] = arr[j + 1], arr[j]
8              yield arr, (j, j+1)
9  yield arr, None""",

    "insertion": """1  for i in range(1, len(arr)):
2      key = arr[i]
3      j = i - 1
4      yield arr, (i,)
5      while j >= 0 and key < arr[j]:
6          arr[j+1] = arr[j]
7          yield arr, (j, j+1)
8          j -= 1
9      arr[j+1] = key
10     yield arr, (j+1,)
11 yield arr, None""",

    "merge": """1  def rec(arr, left, right):
2      if left == right:
3          return
4      mid = (left + right) // 2
5      yield from rec(arr, left, mid)
6      yield from rec(arr, mid+1, right)
7      left_temp = arr[left:mid+1]
8      right_temp = arr[mid+1:right+1]
9      i, j = 0, 0
10     k = left
11     while i < len(left_temp) and j < len(right_temp):
12         if left_temp[i] < right_temp[j]:
13             arr[k] = left_temp[i]
14             i += 1
15         else:
16             arr[k] = right_temp[j]
17             j += 1
18         yield arr, (k,)
19         k += 1
20     while i < len(left_temp):
21         arr[k] = left_temp[i]
22         yield arr, (k,)
23         i += 1
24         k += 1
25     while j < len(right_temp):
26         arr[k] = right_temp[j]
27         yield arr, (k,)
28         j += 1
29         k += 1
30 yield from rec(arr, 0, len(arr)-1)
31 yield arr, None"""
        }

        self.algorithm_line_map = {
            "bubble": {
                "outer_loop": 3,
                "inner_loop": 4,
                "yield_highlight": 5,
                "if_condition": 6,
                "swap": 7,
                "yield_swap": 8,
                "final": 9
            },
            "insertion": {
                "outer_loop": 1,
                "key": 2,
                "j_init": 3,
                "yield_key": 4,
                "while_loop": 5,
                "shift": 6,
                "yield_shift": 7,
                "decrement_j": 8,
                "insert_key": 9,
                "yield_insert": 10,
                "final": 11
            },
            "merge": {
            }
        }

        self.current_algorithm = None

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
        self.current_algorithm = "bubble"
        self.description.config(text=self.algorithm_descriptions["bubble"])

        self.code_text.config(state="normal")
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", self.algorithm_pseudocode["bubble"])
        self.code_text.config(state="disabled")

        self.sort_gen = bubble_sort(self.data)
        self.animate_sort_step()    

    def run_insertion_sort(self):
        if not self.data:
            return
        self.current_algorithm = "insertion"
        self.description.config(text=self.algorithm_descriptions["insertion"])

        self.code_text.config(state="normal")
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", self.algorithm_pseudocode["insertion"])
        self.code_text.config(state="disabled")

        self.sort_gen = insertion_sort(self.data)
        self.animate_sort_step()

    def run_merge_sort(self):
        if not self.data:
            return
        self.current_algorithm = "merge"
        self.description.config(text=self.algorithm_descriptions["merge"])

        self.code_text.config(state="normal")
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", self.algorithm_pseudocode["merge"])
        self.code_text.config(state="disabled")

        self.sort_gen = merge_sort(self.data)
        self.animate_sort_step()

    def animate_sort_step(self):
        try:
            arr, highlight = next(self.sort_gen)
            self.data = arr
            self.draw_array(highlight=highlight)

            if self.current_algorithm:
                self.code_text.config(state="normal")
                self.code_text.tag_remove("highlight","1.0", tk.END)

                if self.current_algorithm == "bubble" and highlight is not None:
                    i, j = highlight

                    if arr[i] > arr[j]:
                        line_num = self.algorithm_line_map["bubble"]["swap"]
                    else:
                        line_num = self.algorithm_line_map["bubble"]["if_condition"]

                    self.code_text.tag_add("highlight", f"{line_num}.0", f"{line_num}.end")
                    self.code_text.tag_config("highlight", background="yellow")

                self.code_text.config(state="disabled")                    

            self.canvas.after(self.speed_var.get(), self.animate_sort_step)
        except StopIteration:
            if self.current_algorithm == "bubble":
                self.code_text.config(state="normal")
                final_line = self.algorithm_line_map["bubble"]["final"]
                self.code_text.tag_add("highlight", f"{final_line}.0", f"{final_line}.end")
                self.code_text.tag_config("highlight", background="yellow")
                self.code_text.config(state="disabled")
            return
