from graphs_tradke import sp, heapq

graph = {
    0: {1: 4, 2: 1},
    1: {3: 1},
    2: {1: 2, 3: 5},
    3: {}
}


dist, path = sp.dijkstra(graph, 0)

print("Shortest distances from node 0:", dist)
print("Paths:", path)

bfs_path = sp.bfs(graph, 0)
print("BFS traversal from node 0:", bfs_path)