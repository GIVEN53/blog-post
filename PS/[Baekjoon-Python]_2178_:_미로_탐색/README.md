[Baekjoon-Python] 2178 : 미로 탐색
=
<https://www.acmicpc.net/problem/2178>


접근
--


1. 미로를 bfs 탐색한다.


풀이
--



```python
from sys import stdin
from collections import deque


def bfs(x, y):
    q = deque([(x, y, maze[x][y])])

    while q:
        r, c, cnt = q.popleft()
        cnt += 1
        for i in range(4):
            nr, nc = r + direction[i], c + direction[3 - i]
            if is_out_of_range(nr, nc):
                continue
            if maze[nr][nc] == 0 or maze[nr][nc] > cnt: # (1)
                maze[nr][nc] = cnt
                q.append((nr, nc, cnt))


def is_out_of_range(r, c):
    return r < 0 or r >= n or c < 0 or c >= m or arr[r][c] == "0"


n, m = map(int, stdin.readline().split())
arr = [stdin.readline().rstrip() for _ in range(n)]

maze = [[0] * m for _ in range(n)]
maze[n - 1][m - 1] = 1
direction = [1, 0, -1, 0]
bfs(n - 1, m - 1)

print(maze[0][0])
```


* (1) 다음 칸을 지나가지 않았거나 지나갔지만 현재가 더 적은 칸을 이동했을 때 큐에 삽입한다.
