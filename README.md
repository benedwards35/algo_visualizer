# Algorithm Visualizer

A Python-based visualization tool for understanding how fundamental algorithms work. Watch sorting and graph traversal algorithms execute step-by-step with detailed explanations.

## Features

### Sorting Algorithms
- **Bubble Sort** - Repeatedly swaps adjacent elements if they are in the wrong order
- **Insertion Sort** - Builds a sorted array one element at a time by inserting elements in their correct position
- **Merge Sort** - Recursively splits the array into halves, sorts each half, and merges them back together

### Graph Algorithms
- **Breadth-First Search (BFS)** - Explores nodes level by level, visiting all neighbors before moving deeper
- **Depth-First Search (DFS)** - Explores as far as possible along each branch before backtracking
- **Dijkstra's Algorithm** - Finds the shortest path between nodes by repeatedly selecting the unvisited node with the smallest distance

## Installation

### Requirements
- Python 3.7 or higher
- tkinter (usually included with Python)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/benedwards35/algo_visualizer.git
cd algo_visualizer
```

2. No additional dependencies are required. The project uses only Python standard library.

## Usage

### Running the Application

```bash
python main.py
```

The application will open a window with three tabs: **Sorting**, **Graphs**, and **Trees**.

### Sorting Tab

1. Click **"Generate Random Array"** to create a new array
2. Adjust the array size (2-40 elements) and animation speed (1-1000ms) as needed
3. Select a sorting algorithm button to begin visualization
4. Use **Pause** to pause the animation, **Resume** to continue, or **Reset** to start over
5. Watch the algorithm execute with highlighted comparisons and step-by-step instructions

### Graph Tab

1. Click **"Generate Random Graph"** to create a new graph
2. Adjust the number of nodes (2-20) and animation speed as needed
3. Select a graph algorithm (BFS, DFS, or Dijkstra) to begin visualization
4. Watch nodes light up in red as they are visited, with detailed explanations of each step
5. Use **Pause**, **Resume**, and **Reset** controls

## Project Structure

```
algo_visualizer/
├── main.py                          # Application entry point
├── README.md                        # This file
├── algorithms/
│   ├── sorting/
│   │   ├── bubble_sort.py
│   │   ├── insertion_sort.py
│   │   └── merge_sort.py
│   └── graph/
│       ├── bfs_search.py
│       ├── dfs_search.py
│       └── dijkstra_algorithm.py
└── ui/
    ├── app.py                       # Main UI application
    ├── sorting_tab.py               # Sorting algorithm visualization
    ├── graph_tab.py                 # Graph algorithm visualization
    └── tree_tab.py                  # Tree algorithm visualization (in development)
```

## How It Works

### Algorithm Generators

Each algorithm is implemented as a Python generator function that yields step-by-step execution states. This allows the UI to control the visualization frame-by-frame:

```python
def bubble_sort(arr):
    # ... algorithm code ...
    yield arr, highlighted_indices, line_number, state
```

### Visualization Loop

The UI's `animate_algorithm_step()` method:
1. Gets the next step from the algorithm generator
2. Updates the visual display (highlights, canvas drawing)
3. Updates the instruction text with detailed explanations
4. Schedules the next animation frame based on speed setting

## Controls

| Control | Function |
|---------|----------|
| Generate/Generate Random | Create new data structure |
| Algorithm Buttons | Start selected algorithm |
| Size/Nodes Spinbox | Adjust data structure size |
| Speed Scale | Control animation speed (1-1000ms) |
| Pause | Pause the current animation |
| Resume | Continue paused animation |
| Reset | Return to initial state |

## Customization

### Adjusting Animation Speed
The speed scale controls the delay between animation frames (in milliseconds). Lower values = faster animation.

### Adding New Algorithms
To add a new sorting algorithm:
1. Create a generator function in `algorithms/sorting/`
2. Import it in `sorting_tab.py`
3. Add a button and description
4. Implement instruction mappings for detailed explanations

## Future Plans

- Tree algorithms visualization (BST, AVL, Red-Black trees)
- Dark mode and smooth animations
- Weighted graph support
- Custom graph input
- Algorithm complexity analysis
- Code execution viewer

## Technologies Used

- **Python 3.x** - Core language
- **tkinter** - GUI framework
- **Collections.deque** - Queue for BFS
- **heapq** - Priority queue for Dijkstra's algorithm

## License

This project is open source and available under the MIT License.

## Author

Benjamin Edwards (@benedwards35)

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for bugs and feature requests.
