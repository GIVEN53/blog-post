[Baekjoon-Python] 1613 : 역사
=
<https://www.acmicpc.net/problem/1613>


접근
--


1. a(전 관계) b(후 관계)가 있을 때 dfs 탐색하여 b의 후 관계로 있는 사건을 a의 후 관계로 압축한다.


풀이
--



```python
from sys import stdin


def dfs(start):
    if visited[start]:
        return

    visited[start] = True # (1)
    for end in graph[start]:
        dfs(end)
        event[start].add(end)
        event[start] |= event[end] # (2)


n, k = map(int, stdin.readline().split())
graph = [[] for _ in range(n + 1)]
for _ in range(k):
    a, b = map(int, stdin.readline().split())
    graph[a].append(b)

event = [set() for _ in range(n + 1)]
visited = [False] * (n + 1)
for i in range(1, n + 1):
    dfs(i) # (3)

s = int(stdin.readline())
for _ in range(s):
    start, end = map(int, stdin.readline().split())
    if end in event[start]:
        print(-1)
    elif start in event[end]:
        print(1)
    else:
        print(0)
```


* (1) 방문 처리해서 이미 탐색한 사건은 중복 탐색하지 않는다.
* (2) 관계를 압축한다.
* (3) 모든 사건을 dfs 탐색한다.
