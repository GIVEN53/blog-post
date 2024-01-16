[Baekjoon-Python] 1167 : 트리의 지름
=
<https://www.acmicpc.net/problem/1167>


접근
--


1. 임의의 노드 x에서 가장 먼 노드 y를 찾은 후, 노드 y에서 가장 먼 노드 z까지의 거리를 구한다.
2. 트리 구조는 중간 경로를 공유하기 때문에 두 번의 탐색으로 트리의 지름을 구할 수 있고, 첫 탐색은 어떤 노드를 선택해도 상관없다.


풀이
--



```python
from sys import stdin


def dfs(now, diameter):
    for next, d in graph[now].items():
        if visited[next] == -1:
            visited[next] = diameter + d
            dfs(next, visited[next])


V = int(stdin.readline())
graph = [{} for _ in range(V + 1)]
for _ in range(V):
    edges = [*map(int, stdin.readline().split()[:-1])]
    node = edges[0]

    for i in range(2, len(edges), 2):
        graph[node][edges[i - 1]] = edges[i]

visited = [-1] * (V + 1)
visited[1] = 0
dfs(1, visited[1]) # (1)

start = visited.index(max(visited)) # (2)
visited = [-1] * (V + 1)
visited[start] = 0
dfs(start, visited[start]) # (3)

print(max(visited))
```


* (1) 임의의 노드를 1로 설정하고 탐색한다.
* (2) 노드 1과 가장 먼 노드를 찾는다.
* (3) 두 번째 탐색을 진행한다.
