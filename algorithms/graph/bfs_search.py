from collections import deque

def bfs_search(graph, start=0):
    visited = set()
    queue = deque()
    
    queue.append(start)
    visited.add(start)
    
    state = {
        "current_node": start,
        "visited": list(visited),
        "queue": list(queue)
    }
    yield graph, [start], 1, state
    
    while queue:
        current = queue.popleft()
        
        state = {
            "current_node": current,
            "visited": list(visited),
            "queue": list(queue)
        }
        yield graph, [current], 2, state
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
                state = {
                    "current_node": current,
                    "visited": list(visited),
                    "queue": list(queue)
                }
                yield graph, list(visited), 3, state
    
    state = {
        "current_node": -1,
        "visited": list(visited),
        "queue": []
    }
    yield graph, list(visited), 5, state
