[Baekjoon-Python] 2252 : 줄 세우기
=
<https://www.acmicpc.net/problem/2252>


접근
--


1. 위상 정렬 알고리즘을 사용한다.


풀이
--



```python
from sys import stdin
from collections import deque


def topological_sort():
    q = deque()
    for i in range(1, N + 1):
        if in_degree[i] == 0:
            q.append(i) # (1)

    while q:
        node = q.popleft()
        print(node, end=" ")

        for i in graph[node]: # (2)
            in_degree[i] -= 1
            if in_degree[i] == 0:
                q.append(i)


N, M = map(int, stdin.readline().split())
graph = [[] for _ in range(N + 1)]
in_degree = [0] * (N + 1)

for _ in range(M):
    a, b = map(int, stdin.readline().split())
    graph[a].append(b)
    in_degree[b] += 1 # (3)

topological_sort()
```


* (1) 진입 차수가 0인 노드를 큐에 삽입한다.
* (2) 다음 노드를 순회하면서 진입 차수를 1씩 감소시키고, 진입 차수가 0이면 큐에 삽입한다.
* (3) a -> b 간선이 존재할 때 b의 진입 차수가 증가한다.
