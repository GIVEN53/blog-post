[Baekjoon-Python] 21610 : 마법사 상어와 비바라기
=
<https://www.acmicpc.net/problem/21610>


접근
--


1. 격자의 끝이 연결되어 있기 때문에 구름이 이동할 때 n으로 나눈 나머지만큼 이동한다.
2. 이동한 구름 좌표를 저장해서 물복사버그를 사용할 때 좌표의 대각선을 순회하고, 새로운 구름을 생성할 때 좌표가 포함되었는지 확인한다.


풀이
--



```python
from sys import stdin
from collections import deque


def move_cloud(move_r, move_c) -> set:
    moved_cloud = set()
    while cloud:
        r, c = cloud.popleft()

        r, c = (r + move_r) % n, (c + move_c) % n # (1)
        board[r][c] += 1
        moved_cloud.add((r, c))
    return moved_cloud


def copy_diagonal(moved_cloud: set):
    for r, c in moved_cloud:
        cnt = 0
        for d in range(1, 8, 2): # (2)
            nr, nc = r + direction[d][0], c + direction[d][1]
            if 0 <= nr < n and 0 <= nc < n and board[nr][nc]:
                cnt += 1
        board[r][c] += cnt # (3)


def create_cloud(moved_cloud: set):
    for i in range(n):
        for j in range(n):
            if board[i][j] < 2 or (i, j) in moved_cloud:
                continue
            cloud.append((i, j))
            board[i][j] -= 2


n, m = map(int, stdin.readline().split())
board = [list(map(int, stdin.readline().split())) for _ in range(n)]

cloud = deque([(n - 1, 0), (n - 1, 1), (n - 2, 0), (n - 2, 1)])
direction = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
for _ in range(m):
    d, s = map(int, stdin.readline().split())
    move_r, move_c = direction[d - 1][0] * s, direction[d - 1][1] * s
    moved_cloud = move_cloud(move_r, move_c)
    copy_diagonal(moved_cloud)
    create_cloud(moved_cloud)

print(sum(sum(b) for b in board))
```


* (1) 양 끝이 연결되어 있으므로 n으로 나눈 나머지를 구한다.
* (2) 대각선 방향만 순회한다.
* (3) 대각선 방향으로 거리가 1인 칸에 물이 있는 바구니 개수만큼 물의 양을 증가시킨다.
