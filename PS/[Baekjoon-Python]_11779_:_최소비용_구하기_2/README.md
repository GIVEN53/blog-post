[Baekjoon-Python] 11779 : 최소비용 구하기 2
=
<https://www.acmicpc.net/problem/11779>


접근
--


1. 다익스트라 알고리즘을 사용하여 출발 도시에서 도착 도시까지 가는데 발생하는 최소 비용을 구한다.
2. 현재 노드에서 다음 노드로 갈 때 최소 비용이면 다음 노드에 현재 노드 번호를 저장한다.


풀이
--



```python
from sys import stdin
from heapq import heappush, heappop


def dijkstra(start):
    q = []
    heappush(q, (0, start))
    while q:
        dist, now = heappop(q)

        for next, next_dist in graph[now].items():
            cost = dist + next_dist
            if cost < distance[next]:
                distance[next], log[next] = cost, now # (1)
                heappush(q, (cost, next))


n = int(stdin.readline())
m = int(stdin.readline())
graph = [{} for _ in range(n + 1)]
for _ in range(m):
    a, b, c = map(int, stdin.readline().split())
    if b not in graph[a] or c < graph[a][b]: # (2)
        graph[a][b] = c

start, end = map(int, stdin.readline().split())
distance = [1e9] * (n + 1)
log = [0] * (n + 1)

dijkstra(start)
print(distance[end])

ans = [end]
while end != start:
    end = log[end]
    ans.append(end)
ans.reverse()

print(len(ans))
print(*ans)
```


* (1) 비용과 노드 번호를 저장한다.
* (2) 중복된 간선이 존재하기 때문에 dictionary를 사용할 경우 최소 비용인 간선을 저장한다.
