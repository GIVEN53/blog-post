[Baekjoon-Python] 2468 : 안전 영역
=
<https://www.acmicpc.net/problem/2468>


접근
--


1. 비의 양을 `0 ~ 지역의 최고 높이 - 1`까지 순회하면서 안전한 영역의 개수를 구한다.
2. 안전한 영역은 bfs 탐색한다.


풀이
--



```python
from sys import stdin
from collections import deque


def bfs(r, c, rain, q: deque):
    q.append((r, c))

    while q:
        r, c = q.popleft()
        for i in range(4):
            nr, nc = r + direction[i], c + direction[3 - i]
            if is_out_of_range(nr, nc) or visited[nr][nc] or city[nr][nc] <= rain: # (1)
                continue
            visited[nr][nc] = True
            q.append((nr, nc))


def is_out_of_range(r, c):
    return r < 0 or r >= n or c < 0 or c >= n


n = int(stdin.readline())
max_height = 0
city = []
for _ in range(n):
    c = list(map(int, stdin.readline().split()))
    max_height = max(max_height, max(c)) # (2)
    city.append(c)

direction = [1, 0, -1, 0]
q = deque()
res = 0
for rain in range(max_height):
    visited = [[False] * n for _ in range(n)]
    area = 0
    for r in range(n):
        for c in range(n):
            if not visited[r][c] and city[r][c] > rain: # (3)
                visited[r][c] = True
                bfs(r, c, rain, q)
                area += 1
    res = max(res, area)

print(res)
```


* (1) 범위를 벗어났거나 방문했거나 물에 잠긴 지역일 경우 건너뛴다.
* (2) 지역의 최고 높이를 갱신한다.
* (3) 방문하지 않았고 물에 잠기지 않은 지역일 때 안전한 영역을 bfs 탐색한다.
