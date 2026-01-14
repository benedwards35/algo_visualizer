import tkinter as tk
from ui.app import MainApp

def main():
    root = tk.Tk()
    root.geometry("1200x600")
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

'''
Backlog:
✓ Graph Algorithms: "Backend" - BFS, DFS, Dijkstra implemented
✓ Graph Algorithms: Frontend - Full integration with animations
✓ graph_tab.py - Complete with step-by-step visualizations

- Tree Algorithms: "Backend"
- Tree Algorithms: Frontend
- tree_tab.py

- UI/UX Design
- Dark Mode, Smooth Animations
'''