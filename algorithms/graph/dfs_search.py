def dfs_search(graph, start=0):
    visited = set()
    stack = []
    
    stack.append(start)
    
    state = {
        "current_node": start,
        "visited": [],
        "stack": list(stack)
    }
    yield graph, [start], 1, state
    
    while stack:
        current = stack.pop()
        
        if current not in visited:
            visited.add(current)
            
            state = {
                "current_node": current,
                "visited": list(visited),
                "stack": list(stack)
            }
            yield graph, [current], 2, state
            
            for neighbor in reversed(graph[current]):
                if neighbor not in visited:
                    stack.append(neighbor)
                    
                    state = {
                        "current_node": current,
                        "visited": list(visited),
                        "stack": list(stack)
                    }
                    yield graph, list(visited), 3, state
    
    state = {
        "current_node": -1,
        "visited": list(visited),
        "stack": []
    }
    yield graph, list(visited), 5, state
