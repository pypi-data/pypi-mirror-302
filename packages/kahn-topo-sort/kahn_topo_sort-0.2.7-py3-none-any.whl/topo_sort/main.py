from collections import defaultdict, deque

class Topo_Sort:
    
    RED = '\033[31m'
    GREEN = '\033[32m'
    RESET = '\033[0m'

    def __init__(self):
        pass

        # I: RETURNS GRAPH (dict) AND IN_DEGREE (dict)
    def createGraph(data):
        # Create a Graph and In-Degree
        graph = defaultdict(list)
        in_degree = defaultdict(int)

        # Fill Graph and In-Degree with data
        for sublist in data:
            for i in range(len(sublist) - 1):
                u = sublist[i]
                v = sublist[i + 1]
                # u -> v
                graph[u].append(v)
                in_degree[v] += 1
                if u not in in_degree:
                    in_degree[u] = 0
        
        return graph, in_degree
    

    # I: RETURNS SORTED LIST
    def sort(graph, in_degree):
        # Create a queue with vertex with in_degree = 0
        queue = deque([node for node in in_degree if in_degree[node] == 0])
        sorted_list = []

        # Kahn's algorithm
        while queue:
            node = queue.popleft()
            sorted_list.append(node)

            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:        
                    queue.append(neighbor)
        
        # Check for cycles
        if len(sorted_list) == len(in_degree):
            return sorted_list
        else:
            return 'CYCLE IN DATA'
    

    # I: RETURNS FILTERED LIST
    def filterList(ls, use):
        if ls == 'CYCLE IN DATA':
            return '\033[31m' + ls + '\033[0m'
        new_ls = []
        for elem in ls:
            if elem in use:
                new_ls.append(elem)

        return '\033[32m' + str(new_ls) + '\033[0m'