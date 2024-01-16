[Baekjoon-Python] 1504 : 특정한 최단 경로
=
<https://www.acmicpc.net/problem/1504>


접근
--


1. 다익스트라 알고리즘으로 1, u, v의 정점에서 모든 정점까지의 최단 경로를 구한다.
2. 1 -> u -> v -> N, 1 -> v -> u -> N 경로 중 최솟값을 구한다.
3. 경로가 없을 때는 두 개 이상의 네트워크가 존재할 때이다.


풀이
--



```python
from sys import stdin
from heapq import heappop, heappush


def dijkstra(start):
    distance = [1e9] * (N + 1)
    distance[start] = 0
    q = []
    heappush(q, (0, start))
    while q:
        dist, node = heappop(q)
        if distance[node] < dist:
            continue

        for next, next_dist in graph[node].items():
            cost = next_dist + dist
            if cost < distance[next]:
                distance[next] = cost
                heappush(q, (cost, next))

    return distance


N, E = map(int, stdin.readline().split())
graph = [{} for _ in range(N + 1)]

for _ in range(E):
    a, b, c = map(int, stdin.readline().split())
    graph[a][b] = c
    graph[b][a] = c
u, v = map(int, stdin.readline().split())
distance_1 = dijkstra(1)
distance_u = dijkstra(u)
distance_v = dijkstra(v)

u_first = distance_1[u] + distance_u[v] + distance_v[N] # (1)
v_first = distance_1[v] + distance_v[u] + distance_u[N] # (2)
min_distance = min(u_first, v_first)
print(min_distance if min_distance < 1e9 else -1) # (3)
```


* (1) 1 -> u -> v -> N 경로
* (2) 1 -> v -> u -> N 경로
* (3) 경로가 없을 때는 초기화한 값인 1e9이다.
