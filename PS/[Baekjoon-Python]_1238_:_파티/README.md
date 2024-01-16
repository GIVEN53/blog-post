[Baekjoon-Python] 1238 : 파티
=
<https://www.acmicpc.net/problem/1238>


접근
--


1. 다익스트라 알고리즘을 사용한다.
2. 정방향 그래프를 탐색해서 X에서 각각의 노드까지 가는 최단 경로를 구한다.
3. 역방향 그래프를 탐색해서 각각의 노드에서 X까지 가는 최단 경로를 구한다.
4. 두 경로를 더한다.


풀이
--



```python
from sys import stdin
from heapq import heappop, heappush


def dijkstra(start, graph):
    distance = [1e9] * (N + 1)
    distance[start] = 0
    q = []
    heappush(q, (0, start))
    while q:
        dist, node = heappop(q)
        for next, next_dist in graph[node].items():
            cost = dist + next_dist
            if cost < distance[next]:
                distance[next] = cost
                heappush(q, (cost, next))

    return distance


N, M, X = map(int, stdin.readline().split())
graph = [{} for _ in range(N + 1)]
reverse_graph = [{} for _ in range(N + 1)]
for _ in range(M):
    a, b, t = map(int, stdin.readline().split())
    graph[a][b] = t
    reverse_graph[b][a] = t

distance = dijkstra(X, graph)
reverse_distance = dijkstra(X, reverse_graph)
max_distance = 0
for i in range(1, N + 1):
    max_distance = max(max_distance, distance[i] + reverse_distance[i])
print(max_distance)
```

