[Baekjoon-Python] 1948 : 임계경로
=
<https://www.acmicpc.net/problem/1948>


접근
--


* 위상 정렬 알고리즘을 사용해서 각 도시까지 도달하는 최대 시간을 구한다.
* 현재 간선이 다음 도시로 가는 최대 시간이라면 다음 도시에 현재 도시를 저장한다.
* 도착 도시부터 시작하여 저장된 도시의 간선을 탐색해서 간선의 개수를 구한다.


풀이
--



```python
from sys import stdin
from collections import deque


def topological_sort(start):
    q = deque([(start, 0)])
    while q:
        now, dist = q.popleft()

        for next, next_dist in graph[now].items():
            in_degree[next] -= 1
            cost = dist + next_dist
            if distance[next] < cost: # (1)
                distance[next] = cost
                max_dist_nodes[next] = [now]
            elif distance[next] == cost: # (2)
                max_dist_nodes[next].append(now)

            if in_degree[next] == 0: # (3)
                q.append((next, distance[next]))


def get_edge_cnt(start):
    q = deque([start])
    edges = set()
    while q:
        now = q.popleft()

        for next in max_dist_nodes[now]:
            if (now, next) not in edges: # (4)
                edges.add((now, next))
                q.append(next)

    return len(edges)


n, m = int(stdin.readline()), int(stdin.readline())
graph = [{} for _ in range(n + 1)]
in_degree = [0] * (n + 1)

for _ in range(m):
    s, e, t = map(int, stdin.readline().split())
    graph[s][e] = t
    in_degree[e] += 1
start, end = map(int, stdin.readline().split())

distance = [0] * (n + 1)
max_dist_nodes = [[] for _ in range(n + 1)]
topological_sort(start)

print(distance[end])
print(get_edge_cnt(end))
```


* (1) 현재 간선이 다음 도시로 가는 최대 시간이면 리스트를 비우고 현재 도시를 저장한다.
* (2) 현재 간선이 다음 도시로 가는 최대 시간과 같다면 리스트에 현재 도시를 추가한다. (같은 시간으로 다음 도시까지 가는 간선이 여러 개 존재)
* (3) 진입 차수가 0인 노드를 큐에 삽입한다.
* (4) 중복된 간선은 큐에 삽입하지 않는다. 1 -> 2 -> 4, 1 -> 2 -> 3 -> 4 경로가 최대 시간일 때 1 -> 2 간선을 두 번 탐색하는 경우가 발생하기 때문이다.
