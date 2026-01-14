import tkinter as tk
from tkinter import ttk
import random
import math
from algorithms.graph.bfs_search import bfs_search
from algorithms.graph.dfs_search import dfs_search
from algorithms.graph.dijkstra_algorithm import dijkstra_algorithm

class GraphTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        control_frame = tk.Frame(self.frame)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Button(control_frame, text="Generate Random Graph", command=self.generate_graph).pack(pady=5)

        graph_buttons_frame = tk.Frame(control_frame)
        graph_buttons_frame.pack(pady=10)
        tk.Label(graph_buttons_frame, text="Graph Algorithms:").pack(pady=5)
        tk.Button(graph_buttons_frame, text="BFS", command=self.run_bfs).pack(pady=5)
        tk.Button(graph_buttons_frame, text="DFS", command=self.run_dfs).pack(pady=5)
        tk.Button(graph_buttons_frame, text="Dijkstra", command=self.run_dijkstra).pack(pady=5)

        control_buttons_frame = tk.Frame(control_frame)
        control_buttons_frame.pack(pady=15)
        tk.Label(control_buttons_frame, text="Controls:").pack(pady=5)

        tk.Label(control_buttons_frame, text="Number of Nodes (max 20)").pack(pady=2)
        self.nodes_var = tk.IntVar(value=8)
        self.nodes_spinbox = tk.Spinbox(control_buttons_frame, from_=2, to=20, textvariable=self.nodes_var)
        self.nodes_spinbox.pack(pady=2)

        tk.Label(control_buttons_frame, text="Algorithm Speed (ms)").pack(pady=2)
        self.speed_var = tk.IntVar(value=100)
        self.speed_scale = tk.Scale(control_buttons_frame, from_=1, to=1000, orient="horizontal", variable=self.speed_var)
        self.speed_scale.pack(pady=2)

        self.pause_resume_btn = tk.Button(
            control_buttons_frame, 
            text="Pause", 
            command=self.toggle_pause,
            state="disabled",
            width=10
        )
        self.pause_resume_btn.pack(side="left", padx=5, pady=10)

        self.reset_btn = tk.Button(
            control_buttons_frame, 
            text="Reset", 
            command=self.reset_algorithm,
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
            text="Click on a Graph Algorithm to view its description.",
            wraplength=250,
            justify="center"
        )

        self.algorithm_descriptions = {
            "bfs": "Breadth-First Search explores nodes level by level, visiting all neighbors before moving deeper into the graph.",
            "dfs": "Depth-First Search explores as far as possible along each branch before backtracking, using a stack structure.",
            "dijkstra": "Dijkstra's Algorithm finds the shortest path between nodes by repeatedly selecting the unvisited node with the smallest distance."
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
            "bfs": {
                "state": {"current_node": 0, "visited": [], "queue": []},
                "lines": {
                    1: lambda s: [
                        f"Initializing BFS from node {s.get('current_node', 0)}",
                        "Adding start node to queue",
                        "Marking node as visited"
                    ],
                    2: lambda s: [
                        f"Processing node {s.get('current_node', 0)} from queue",
                        "Exploring all unvisited neighbors",
                        f"Queue: {s.get('queue', [])}"
                    ],
                    3: lambda s: [
                        f"Adding unvisited neighbors to queue",
                        f"Visited so far: {s.get('visited', [])}",
                        "Continuing level-order exploration"
                    ],
                    5: lambda s: [
                        "✓ BFS Complete!",
                        f"Visited all {len(s.get('visited', []))} reachable nodes",
                        "Traversal finished in breadth-first order"
                    ]
                }
            },
            "dfs": {
                "state": {"current_node": 0, "visited": [], "stack": []},
                "lines": {
                    1: lambda s: [
                        f"Initializing DFS from node {s.get('current_node', 0)}",
                        "Pushing start node onto stack",
                        "Preparing for depth-first exploration"
                    ],
                    2: lambda s: [
                        f"Processing node {s.get('current_node', 0)} from stack",
                        "Marking as visited",
                        f"Stack: {s.get('stack', [])}"
                    ],
                    3: lambda s: [
                        f"Pushing unvisited neighbors onto stack",
                        f"Visited so far: {s.get('visited', [])}",
                        "Going deeper into the graph"
                    ],
                    5: lambda s: [
                        "✓ DFS Complete!",
                        f"Visited all {len(s.get('visited', []))} reachable nodes",
                        "Traversal finished in depth-first order"
                    ]
                }
            },
            "dijkstra": {
                "state": {"current_node": 0, "visited": [], "distances": {}},
                "lines": {
                    1: lambda s: [
                        f"Starting Dijkstra from node {s.get('current_node', 0)}",
                        "Initializing distances: start=0, others=∞",
                        "Setting up priority queue"
                    ],
                    3: lambda s: [
                        f"Selected node {s.get('current_node', 0)} with distance {s.get('current_distance', 0)}",
                        f"Visited: {s.get('visited', [])}",
                        "Processing neighbors for path updates"
                    ],
                    4: lambda s: [
                        f"Updating distance to node {s.get('updated_neighbor', -1)}",
                        f"New distance: {s.get('distances', {}).get(s.get('updated_neighbor', -1), '∞')}",
                        "Found shorter path through current node"
                    ],
                    7: lambda s: [
                        "✓ Dijkstra Complete!",
                        f"Shortest paths found for {len(s.get('visited', []))} nodes",
                        "All distances are finalized"
                    ]
                }
            }
        }

        self.current_algorithm = None

        self.description_label.pack(pady=(5,0), fill="x")
        self.description.pack(pady=5, fill="x")
        self.instruction_label.pack(pady=(15, 5), fill="x")
        self.instruction_text.pack(pady=5, fill="both", expand=True)
        self.canvas.pack(side="left", padx=10, pady=10)
        self.info_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.graph = {}
        self.graph_gen = None

        self.original_graph = {}
        self.is_paused = False
        self.is_running = False
        self.after_id = None
        self.node_positions = {}

    def generate_graph(self):
        num_nodes = self.nodes_var.get()
        self.graph = {i: [] for i in range(num_nodes)}
        
        for i in range(num_nodes):
            num_neighbors = random.randint(1, min(3, num_nodes - 1))
            neighbors = random.sample([j for j in range(num_nodes) if j != i], num_neighbors)
            self.graph[i] = neighbors
        
        self.original_graph = {k: v[:] for k, v in self.graph.items()}
        self.draw_graph()
        
        self.instruction_text.config(state="normal")
        self.instruction_text.delete("1.0", tk.END)
        self.instruction_text.insert("1.0", "Graph generated!\n\nSelect an algorithm to begin exploration.")
        self.instruction_text.config(state="disabled")

    def draw_graph(self, highlight_nodes=None, highlight_edges=None):
        self.canvas.delete("all")
        if not self.graph:
            return
        
        c_width = int(self.canvas["width"])
        c_height = int(self.canvas["height"])
        
        num_nodes = len(self.graph)
        radius = 120
        center_x = c_width // 2
        center_y = c_height // 2
        
        self.node_positions = {}
        for i in range(num_nodes):
            angle = 2 * math.pi * i / num_nodes
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[i] = (x, y)
        
        for node, neighbors in self.graph.items():
            x1, y1 = self.node_positions[node]
            for neighbor in neighbors:
                x2, y2 = self.node_positions[neighbor]
                edge_color = "red" if highlight_edges and (node, neighbor) in highlight_edges else "gray"
                self.canvas.create_line(x1, y1, x2, y2, fill=edge_color, width=2)
        
        node_radius = 20
        for i, (x, y) in self.node_positions.items():
            node_color = "red" if highlight_nodes and i in highlight_nodes else "turquoise"
            self.canvas.create_oval(x - node_radius, y - node_radius, 
                                   x + node_radius, y + node_radius,
                                   fill=node_color, outline="black", width=2)
            self.canvas.create_text(x, y, text=str(i), font=("Arial", 12, "bold"), fill="white")

    def run_bfs(self):
        if not self.graph:
            return
        self.current_algorithm = "bfs"
        self.description.config(text=self.algorithm_descriptions["bfs"])
        
        self.graph = {k: v[:] for k, v in self.original_graph.items()}
        self.graph_gen = bfs_search(self.graph)
        self.is_running = True
        self.is_paused = False
        self.pause_resume_btn.config(state="normal", text="Pause")
        self.reset_btn.config(state="normal")
        self.animate_algorithm_step()

    def run_dfs(self):
        if not self.graph:
            return
        self.current_algorithm = "dfs"
        self.description.config(text=self.algorithm_descriptions["dfs"])
        
        self.graph = {k: v[:] for k, v in self.original_graph.items()}
        self.graph_gen = dfs_search(self.graph)
        self.is_running = True
        self.is_paused = False
        self.pause_resume_btn.config(state="normal", text="Pause")
        self.reset_btn.config(state="normal")
        self.animate_algorithm_step()

    def run_dijkstra(self):
        if not self.graph:
            return
        self.current_algorithm = "dijkstra"
        self.description.config(text=self.algorithm_descriptions["dijkstra"])
        
        self.graph = {k: v[:] for k, v in self.original_graph.items()}
        self.graph_gen = dijkstra_algorithm(self.graph)
        self.is_running = True
        self.is_paused = False
        self.pause_resume_btn.config(state="normal", text="Pause")
        self.reset_btn.config(state="normal")
        self.animate_algorithm_step()

    def animate_algorithm_step(self):
        if self.is_paused:
            return
        try:
            result = next(self.graph_gen)
            
            if len(result) == 4:
                graph, highlight_nodes, line_num, state = result
            else:
                graph, highlight_nodes = result
                line_num = None
                state = {}
            
            self.graph = graph
            self.draw_graph(highlight_nodes=highlight_nodes)

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

            self.after_id = self.canvas.after(self.speed_var.get(), self.animate_algorithm_step)
            
        except StopIteration:
            self.is_running = False
            self.pause_resume_btn.config(state="disabled", text="Pause")
            self.reset_btn.config(state="disabled")
            return
        
    def toggle_pause(self):
        if self.is_running:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.pause_resume_btn.config(text="Resume")
                if self.after_id:
                    self.canvas.after_cancel(self.after_id)
                    self.after_id = None
            else:
                self.pause_resume_btn.config(text="Pause")
                self.animate_algorithm_step()

    def reset_algorithm(self):
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None
        self.is_running = False
        self.is_paused = False
        self.graph_gen = None
        self.pause_resume_btn.config(state="disabled", text="Pause")
        self.reset_btn.config(state="disabled")
        
        self.graph = {k: v[:] for k, v in self.original_graph.items()}
        self.draw_graph()