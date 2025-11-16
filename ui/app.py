import tkinter as tk
from tkinter import ttk

from ui.sorting_tab import SortingTab
from ui.tree_tab import TreeTab
from ui.graph_tab import GraphTab

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualizer")

        # Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.sorting_tab = SortingTab(self.notebook)
        self.tree_tab = TreeTab(self.notebook)
        self.graph_tab = GraphTab(self.notebook)

        self.notebook.add(self.sorting_tab.frame, text="Sorting")
        self.notebook.add(self.tree_tab.frame, text="Trees")
        self.notebook.add(self.graph_tab.frame, text="Graphs")
