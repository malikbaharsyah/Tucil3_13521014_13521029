import heapq

def astar(adj_list, start, goal, nodes, heuristic):
    visited = set()
    heap = [(0, 0, start, [])]
    while heap:
        (estimated_cost, real_cost, current, path) = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]
        if current == goal:
            path_nodes = [nodes[i] for i in path]
            return real_cost, path_nodes
        for neighbor, weight in adj_list[current]:
            if neighbor not in visited and weight > 0:
                new_real_cost = real_cost + weight
                estimated_cost = new_real_cost + heuristic(neighbor, goal, adj_list)
                heapq.heappush(heap, (estimated_cost, new_real_cost, neighbor, path))
    return None, None

def heuristic(start, goal, adj_list):
    for neighbor, weight in adj_list[start]:
        if neighbor == goal:
            return abs(weight)
    return 0