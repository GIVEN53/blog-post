[Baekjoon-Python] 1916 : 최소비용 구하기
=
<https://www.acmicpc.net/problem/1916>


접근
--


1. 다익스트라 알고리즘을 사용하여 출발 도시에서 도착 도시까지 가는데 발생하는 최소 비용을 구한다.


풀이
--



```python
from sys import stdin
from heapq import heappop, heappush


def dijkstra(start):
    q = []
    heappush(q, (0, start))

    while q:
        dist, now = heappop(q)
        if now == end: # (1)
            break

        for next, next_dist in city[now].items():
            next_dist += dist
            if next_dist < distance[next]:
                distance[next] = next_dist
                heappush(q, (next_dist, next))


n, m = int(stdin.readline()), int(stdin.readline())
city = [{} for _ in range(n + 1)]
for _ in range(m):
    a, b, cost = map(int, stdin.readline().split())
    if b in city[a]:
        city[a][b] = min(city[a][b], cost) # (2)
    else:
        city[a][b] = cost

start, end = map(int, stdin.readline().split())

distance = [1e9] * (n + 1)
dijkstra(start)

print(distance[end])
```


* (1) 도착 도시이면 탈출한다.
* (2) 중복된 버스가 존재하기 때문에 최솟값을 저장한다.
