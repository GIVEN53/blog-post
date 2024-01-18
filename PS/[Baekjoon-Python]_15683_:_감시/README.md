[Baekjoon-Python] 15683 : 감시
=
<https://www.acmicpc.net/problem/15683>


접근
--


1. 각각의 cctv마다 감시할 수 있는 경우의 수

| cctv | 경우의 수 |
| --- | --- |
| 1번 | 4 |
| 2번 | 2 |
| 3번 | 4 |
| 4번 | 4 |
| 5번 | 1 |
2. cctv를 dfs 탐색해서 감시할 수 있는 모든 경우의 수를 구한다.
3. 탐색이 끝나면 사각 지대의 크기를 구한다.


풀이
--



```python
from sys import stdin


def dfs(office, idx):
    global res

    if idx >= len(cctv):
        blind_spot = sum(o.count(0) for o in office)
        res = min(res, blind_spot) # (1)
        return

    r, c = cctv[idx]
    if office[r][c] == 1: # (2)
        for i in range(4):
            tmp_office = [o[:] for o in office]
            watch(tmp_office, r, c, direction[i][0], direction[i][1])
            dfs(tmp_office, idx + 1)
    elif office[r][c] == 2: # (3)
        for i in range(2):
            tmp_office = [o[:] for o in office]
            watch(tmp_office, r, c, direction[i][0], direction[i][1])
            watch(tmp_office, r, c, -direction[i][0], -direction[i][1])
            dfs(tmp_office, idx + 1)
    elif office[r][c] == 3: # (4)
        for i in range(4):
            tmp_office = [o[:] for o in office]
            watch(tmp_office, r, c, direction[i][0], direction[i][1])
            watch(tmp_office, r, c, direction[(i + 1) % 4][0], direction[(i + 1) % 4][1])
            dfs(tmp_office, idx + 1)
    elif office[r][c] == 4: # (5)
        for i in range(4):
            tmp_office = [o[:] for o in office]
            watch(tmp_office, r, c, direction[i][0], direction[i][1])
            watch(tmp_office, r, c, direction[(i + 1) % 4][0], direction[(i + 1) % 4][1])
            watch(tmp_office, r, c, direction[(i + 2) % 4][0], direction[(i + 2) % 4][1])
            dfs(tmp_office, idx + 1)
    else: # (6)
        for i in range(4):
            watch(office, r, c, direction[i][0], direction[i][1])
        dfs(office, idx + 1)


def watch(office, r, c, dr, dc): # (7)
    while True:
        r += dr
        c += dc
        if r < 0 or r >= n or c < 0 or c >= m or office[r][c] == 6:
            break

        if office[r][c] == 0:
            office[r][c] = '#'


n, m = map(int, stdin.readline().split())
office = []
cctv = []
for i in range(n):
    o = list(map(int, stdin.readline().split()))
    for j in range(m):
        if 0 < o[j] < 6:
            cctv.append((i, j))
    office.append(o)

res = 1e9
direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dfs(office, 0)

print(res)
```


* (1) 사각 지대의 크기를 구해서 최솟값을 갱신한다.
* (2) 1번 cctv일 경우 `watch()` 1번 호출 (한 방향 감시), dfs 4번 탐색 (경우의 수 4)
* (3) 2번 cctv일 경우 `watch()` 2번 호출 (두 방향 감시), dfs 2번 탐색 (경우의 수 2)
* (4) 3번 cctv일 경우 `watch()` 2번 호출 (두 방향 감시), dfs 4번 탐색 (경우의 수 4)
* (5) 4번 cctv일 경우 `watch()` 3번 호출 (세 방향 감시), dfs 4번 탐색 (경우의 수 4)
* (6) 5번 cctv일 경우 `watch()` 4번 호출 (네 방향 감시), dfs 1번 탐색 (경우의 수 1)
* (7) 범위를 벗어가거나 벽을 만날 때까지 감시 영역을 표시한다.
