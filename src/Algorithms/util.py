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