import heapq

def dijkstra_algorithm(graph, start=0):
    num_nodes = len(graph)
    distances = {i: float('inf') for i in range(num_nodes)}
    distances[start] = 0
    visited = set()
    pq = [(0, start)]
    
    state = {
        "current_node": start,
        "visited": [],
        "distances": distances.copy(),
        "current_distance": 0
    }
    yield graph, [start], 1, state
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        state = {
            "current_node": current,
            "visited": list(visited),
            "distances": distances.copy(),
            "current_distance": current_dist
        }
        yield graph, list(visited), 3, state
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                new_distance = distances[current] + 1
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))
                    
                    state = {
                        "current_node": current,
                        "visited": list(visited),
                        "distances": distances.copy(),
                        "current_distance": current_dist,
                        "updated_neighbor": neighbor
                    }
                    yield graph, list(visited), 4, state
    
    state = {
        "current_node": -1,
        "visited": list(visited),
        "distances": distances.copy(),
        "current_distance": 0
    }
    yield graph, list(visited), 7, state
