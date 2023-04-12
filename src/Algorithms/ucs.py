import heapq
import matplotlib.pyplot as plt
import networkx as nx
    
def ucs(adj_list, start, goal, nodes):
    visited = set()
    heap = [(0, start, [])]
    while heap:
        (cost, current, path) = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]
        if current == goal:
            path_nodes = [nodes[i] for i in path]
            return cost, path_nodes
        for neighbor, weight in adj_list[current]:
            if neighbor not in visited and weight > 0:
                heapq.heappush(heap, (cost + weight, neighbor, path))
    return None, None

def show_graph(adj_list, path, nodes):
    G = nx.Graph()
    for i in range(len(adj_list)):
        for neighbor, weight in adj_list[i]:
            G.add_edge(nodes[i], nodes[neighbor], weight=weight)

    
    node_colors = ['red' if i in path else 'blue' for node in G.nodes()]
    edge_colors = ['red' if (u, v) in zip(path, path[1:]) or (v, u) in zip(path, path[1:]) else 'black' for u, v in G.edges()]
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, node_color=node_colors, edge_color=edge_colors, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

