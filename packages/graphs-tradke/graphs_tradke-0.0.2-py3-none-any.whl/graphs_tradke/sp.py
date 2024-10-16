import sys
from heapq import heappush, heappop

def dijkstra(graph, source): 
    dist = [sys.maxsize] * len(graph)
    dist[source] = 0
    heap = []
    heappush(heap, (0, source))
    path = {}
    path[source] = []
    while len(heap) > 0:
        w, u = heappop(heap)
        for v in graph[u]:
            if w + graph[u][v] < dist[v]:
                dist[v] = w + graph[u][v]
                heappush(heap, (dist[v], v))
                path[v] = path[u] + [u]
    return dist, path




def bfs(graph, start):
    visited = set()
    queue = [start]
    path = []

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            path.append(node)
            queue.extend(graph[node].keys())

    return path