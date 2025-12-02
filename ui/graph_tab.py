import tkinter as tk
from tkinter import ttk

class GraphTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        tk.Label(self.frame, text="Graph Tab Loaded").pack(padx=20, pady=20)

        control_frame = tk.Frame(self.frame)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Button(control_frame,
                   text="Generate Random Graph",command=self.generate_graph).pack(pady=5)

        self.canvas = tk.Canvas(self.frame, width=700, height=400, bg="white")
        self.canvas.pack(padx=10, pady=10)

        '''
        Backlog:

        - Randomly generate x amount of circles (nodes), with random values
        and random connections. 
        - Implement toggles for unweighted/weighted and undirected/directed
        - Implement DFS, BFS
        - Implement Dijkstra's Algorithm

        '''

    def generate_graph(self):
        self.canvas.create_oval(10,10,80,80, outline="black", fill="white", width=2)