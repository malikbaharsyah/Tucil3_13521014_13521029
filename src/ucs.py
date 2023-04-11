import heapq
import matplotlib.pyplot as plt
import networkx as nx

def read_graph(file_name):
    with open(file_name, 'r') as f:
        n = int(f.readline().strip())
        nodes = f.readline().strip().split(',')
        adj_list = [[] for i in range(n)]
        for i in range(n):
            row = list(map(float, f.readline().strip().split(',')))
            for j, w in enumerate(row):
                if w != 0:
                    adj_list[i].append((j, w))
                    adj_list[j].append((i, w))
        return nodes, adj_list
    
def ucs(adj_list, start, goal):
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
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor, path))
    return None, None
def show_graph(adj_list, path):
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



# Main program
file_name = "graph.txt"
nodes, adj_list = read_graph(file_name)

print("Nodes:", nodes)
print("Adjacency List:")
for i in range(len(adj_list)):
    print(nodes[i], "->", end=" ")
    for neighbor, weight in adj_list[i]:
        print(nodes[neighbor], "(" + str(weight) + ")", end=" ")
    print()

start = input("Enter starting node: ")
while start not in nodes:
    print("Invalid node name. Please enter a valid node name.")
    start = input("Enter starting node: ")
start_index = nodes.index(start)

goal = input("Enter goal node: ")
while goal not in nodes:
    print("Invalid node name. Please enter a valid node name.")
    goal = input("Enter goal node: ")
goal_index = nodes.index(goal)

cost, path = ucs(adj_list, start_index, goal_index)
if path:
    print("Shortest path from", start, "to", goal, ":", path)
    print("Total cost:", cost)
else:
    print("There is no path from", start, "to", goal)

show_graph(adj_list, path)