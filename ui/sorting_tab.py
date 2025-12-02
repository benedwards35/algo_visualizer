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
        self.size_var = tk.IntVar(value=20)
        self.size_spinbox = tk.Spinbox(control_frame, from_=2, to=40, textvariable=self.size_var)
        self.size_spinbox.pack(pady=5)

        tk.Label(control_frame, text="Algorithm Speed (ms)").pack(pady=5)
        self.speed_var = tk.IntVar(value=100)
        self.speed_scale = tk.Scale(control_frame, from_=1, to=1000, orient="horizontal", variable=self.speed_var)
        self.speed_scale.pack(pady=5)

        tk.Button(control_frame, text="Generate Array", command=self.generate_array).pack(pady=5)
        tk.Button(control_frame, text="Bubble Sort", command=self.run_bubble_sort).pack(pady=5)
        tk.Button(control_frame, text="Insertion Sort", command=self.run_insertion_sort).pack(pady=5)
        tk.Button(control_frame, text="Merge Sort", command=self.run_merge_sort).pack(pady=5)

        control_buttons_frame = tk.Frame(control_frame)
        control_buttons_frame.pack(pady=15)

        self.pause_resume_btn = tk.Button(
            control_buttons_frame, 
            text="Pause", 
            command=self.toggle_pause,
            state="disabled",
            width=10
        )
        self.pause_resume_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(
            control_buttons_frame, 
            text="Reset", 
            command=self.reset_sort,
            state="disabled",
            width=10
        )

        self.reset_btn.pack(side="left", padx=5)

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
            justify="center"
        )

        self.algorithm_descriptions = {
            "bubble": "Bubble Sort repeatedly swaps adjacent elements if they are in the wrong order until the list is sorted.",
            "insertion": "Insertion Sort builds a sorted array one element at a time by inserting elements in their correct position.",
            "merge": "Merge Sort recursively splits the array into halves, sorts each half, and merges them back together."
        }

        self.instruction_label = tk.Label(
            self.info_frame,
            text="Current Steps:",
            font=("Arial", 12, "bold"),
            anchor="w",
            justify="left"
        )

        self.instruction_text = tk.Text(
            self.info_frame,
            height=8,
            width=40,
            wrap="word",
            font=("Arial", 11),
            bg="#f8f9fa",
            fg="#212529",
            padx=15,
            pady=15,
            relief="solid",
            borderwidth=2,
            state="disabled"
        )

        self.algorithm_instructions = {
            "bubble": {
                "state": {"outer_i": 0, "inner_j": 0, "n": 0},
                "lines": {
                    3: lambda s: [
                        f"Pass {s['outer_i'] + 1} of {s['n']}",
                        "Bubbling largest unsorted element to the end"
                    ],
                    4: lambda s: [
                        f"Pass {s['outer_i'] + 1} of {s['n']}",
                        f"Comparing adjacent elements (positions {s['inner_j']} and {s['inner_j'] + 1})"
                    ],
                    5: lambda s: [
                        f"Pass {s['outer_i'] + 1} of {s['n']}",
                        f"Examining elements at positions {s['inner_j']} and {s['inner_j'] + 1}",
                        "Checking if they need to be swapped"
                    ],
                    7: lambda s: [
                        f"Pass {s['outer_i'] + 1} of {s['n']}",
                        f"Elements at positions {s['inner_j']} and {s['inner_j'] + 1} are out of order",
                        "✓ Swapping elements"
                    ],
                    9: lambda s: [
                        "✓ Sorting Complete!",
                        f"Array sorted after {s['n']} passes",
                        "All elements are now in ascending order"
                    ]
                }
            },
            "insertion": {
                "state": {"i": 0, "key": 0, "j": 0, "n": 0},
                "lines": {
                    1: lambda s: [
                        f"Building sorted portion: element {s['i']} of {s['n']}",
                        "Expanding the sorted section one element at a time"
                    ],
                    4: lambda s: [
                        f"Inserting element at position {s['i']} (value: {s['key']})",
                        "Finding correct position in sorted portion"
                    ],
                    7: lambda s: [
                        f"Inserting value {s['key']}",
                        f"Shifting element at position {s['j']} one position right",
                        "Making room for the key element"
                    ],
                    10: lambda s: [
                        f"Inserted value {s['key']} at position {s['j'] + 1}",
                        f"Sorted portion now contains {s['i'] + 1} elements",
                        "Moving to next unsorted element"
                    ],
                    11: lambda s: [
                        "✓ Sorting Complete!",
                        f"All {s['n']} elements inserted in correct order",
                        "Array is now fully sorted"
                    ]
                }
            },
            "merge": {
                "state": {"k": 0, "n": 0, "phase": ""},
                "lines": {
                    2: lambda s: [
                        "Recursively splitting array into halves",
                        "Divide phase: breaking down to single elements"
                    ],
                    18: lambda s: [
                        "Conquer phase: Merging sorted subarrays",
                        f"Placing element at position {s['k']}",
                        "Comparing and selecting smaller element"
                    ],
                    22: lambda s: [
                        "Merging remaining elements",
                        f"Copying from left subarray to position {s['k']}",
                        "Left subarray has remaining elements"
                    ],
                    27: lambda s: [
                        "Merging remaining elements",
                        f"Copying from right subarray to position {s['k']}",
                        "Right subarray has remaining elements"
                    ],
                    31: lambda s: [
                        "✓ Sorting Complete!",
                        "All subarrays merged successfully",
                        "Array is now fully sorted"
                    ]
                }
            }
        }

        self.current_algorithm = None

        self.description_label.pack( pady=(5,0), fill="x")
        self.description.pack(pady=5, fill="x")
        self.instruction_label.pack(pady=(15, 5), fill="x")
        self.instruction_text.pack(pady=5, fill="both", expand=True)
        self.canvas.pack(side="left", padx=10, pady=10)
        self.info_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.data = []
        self.sort_gen = None

        self.original_data = []
        self.is_paused = False
        self.is_sorting = False
        self.after_id = None

    def generate_array(self):
        size = self.size_var.get()
        self.data = [random.randint(10, 390) for _ in range(size)]
        self.original_data = self.data[:]
        self.draw_array()
        
        self.instruction_text.config(state="normal")
        self.instruction_text.delete("1.0", tk.END)
        self.instruction_text.insert("1.0", "Array generated!\n\nSelect an algorithm to begin sorting.")
        self.instruction_text.config(state="disabled")

    def draw_array(self, highlight=None):
        self.canvas.delete("all")
        if not self.data:
            return
        
        c_width = int(self.canvas["width"])
        c_height = int(self.canvas["height"])

        label_height = 30
        usable_height = c_height - label_height
        bar_width = c_width / len(self.data)

        for i, height in enumerate(self.data):
            x0 = i * bar_width
            y0 = usable_height - (height * usable_height / 400)
            x1 = (i + 1) * bar_width
            y1 = c_height
            color = "red" if highlight and i in highlight else "turquoise"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

            label_x = (x0 + x1) / 2
            label_y = usable_height + 15
            self.canvas.create_text(
                label_x,
                label_y,
                text=str(i),
                font=("Ariel", 9, "bold"),
                fill="#333333"
            )

    def run_bubble_sort(self):
        if not self.data:
            return
        self.current_algorithm = "bubble"
        self.description.config(text=self.algorithm_descriptions["bubble"])

        self.data = self.original_data[:]
        self.sort_gen = bubble_sort(self.data)
        self.is_sorting = True
        self.is_paused = False
        self.pause_resume_btn.config(state="normal", text="Pause")
        self.reset_btn.config(state="normal")
        self.animate_sort_step()   

    def run_insertion_sort(self):
        if not self.data:
            return
        self.current_algorithm = "insertion"
        self.description.config(text=self.algorithm_descriptions["insertion"])

        self.data = self.original_data[:]
        self.sort_gen = insertion_sort(self.data)
        self.is_sorting = True
        self.is_paused = False
        self.pause_resume_btn.config(state="normal", text="Pause")
        self.reset_btn.config(state="normal")
        self.animate_sort_step()

    def run_merge_sort(self):
        if not self.data:
            return
        self.current_algorithm = "merge"
        self.description.config(text=self.algorithm_descriptions["merge"])

        self.data = self.original_data[:]
        self.sort_gen = merge_sort(self.data)
        self.is_sorting = True
        self.is_paused = False
        self.pause_resume_btn.config(state="normal", text="Pause")
        self.reset_btn.config(state="normal")
        self.animate_sort_step()

    def animate_sort_step(self):
        if self.is_paused:
            return
        try:
            result = next(self.sort_gen)
            
            if len(result) == 4:
                arr, highlight, line_num, state = result
            else:
                arr, highlight = result
                line_num = None
                state = {}
            
            self.data = arr
            self.draw_array(highlight=highlight)

            if self.current_algorithm and line_num is not None:
                instructions_func = self.algorithm_instructions[self.current_algorithm]["lines"].get(line_num)
                
                if instructions_func:
                    instructions = instructions_func(state)
                    
                    self.instruction_text.config(state="normal")
                    self.instruction_text.delete("1.0", tk.END)
                    
                    for idx, instruction in enumerate(instructions):
                        if idx == 0:
                            self.instruction_text.insert(tk.END, f"➤ {instruction}\n\n", "main")
                        else:
                            self.instruction_text.insert(tk.END, f"  • {instruction}\n", "detail")
                    
                    self.instruction_text.tag_config("main", font=("Arial", 11, "bold"), foreground="#0066cc")
                    self.instruction_text.tag_config("detail", font=("Arial", 10), foreground="#495057")
                    
                    self.instruction_text.config(state="disabled")

            self.after_id = self.canvas.after(self.speed_var.get(), self.animate_sort_step)
            
        except StopIteration:
            self.is_sorting = False
            self.pause_resume_btn.config(state="disabled", text="Pause")
            self.reset_btn.config(state="disabled")
            return
        
    def toggle_pause(self):
        if self.is_sorting:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.pause_resume_btn.config(text="Resume")
                if self.after_id:
                    self.canvas.after_cancel(self.after_id)
                    self.after_id = None
            else:
                self.pause_resume_btn.config(text="Pause")
                self.animate_sort_step()

    def reset_sort(self):
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None
        self.is_sorting = False
        self.is_paused = False
        self.sort_gen = None
        self.pause_resume_btn.config(state="disabled", text="Pause")
        self.reset_btn.config(state="disabled")
        
        self.data = self.original_data[:]
        self.draw_array()
