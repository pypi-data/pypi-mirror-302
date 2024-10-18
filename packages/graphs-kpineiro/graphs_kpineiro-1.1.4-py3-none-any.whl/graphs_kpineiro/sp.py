import sys
from heapq import heappush, heappop

def dijkstra(graph, source):
    # Get all nodes from the graph (both keys and values)
    all_nodes = set(graph.keys()).union(*[set(edges.keys()) for edges in graph.values()])
    
    # Initialize dist for all nodes
    dist = {node: sys.maxsize for node in all_nodes}
    dist[source] = 0  # Distance to the source is 0

    heap = []
    heappush(heap, (0, source))
    path = {}
    path[source] = []

    while heap:
        w, u = heappop(heap)
        if u not in graph:
            continue  # Skip nodes with no outgoing edges
        for v in graph[u]:
            if w + graph[u][v] < dist[v]:
                dist[v] = w + graph[u][v]
                heappush(heap, (dist[v], v))
                path[v] = path[u] + [u]

    return dist, path


