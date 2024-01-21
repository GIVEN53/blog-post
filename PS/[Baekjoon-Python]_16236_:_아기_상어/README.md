[Baekjoon-Python] 16236 : 아기 상어
=
<https://www.acmicpc.net/problem/16236>


접근
--


1. bfs 탐색하여 물고기를 찾는다.
2. 상어보다 크기가 작은 물고기를 찾으면 거리와 물고기 좌표를 저장한다.
3. 빈 칸이거나 상어와 크기가 같다면 이동한다.
4. 먹을 수 있는 물고기가 여러 마리라면 거리가 가장 가까운 물고기를,  
 거리가 가장 가까운 물고기가 여러 마리라면 행이 가장 작은 물고기를,  
 행이 가장 작은 물고기가 여러 마리라면 열이 가장 작은 물고기를 먹는다.


풀이
--



```python
from sys import stdin
from collections import deque


def bfs(r, c):
    q = deque([(0, r, c)])
    visited = [[False] * n for _ in range(n)]
    visited[r][c] = True

    eatable_fish = []
    min_dist = 1e9
    while q:
        dist, r, c = q.popleft()
        if dist > min_dist: # (1)
            continue

        dist += 1
        for i in range(4):
            nr, nc = r + direction[i], c + direction[3 - i]
            if is_out_of_range(nr, nc) or visited[nr][nc]:
                continue

            visited[nr][nc] = True
            fish = sea[nr][nc]
            if 0 < fish < shark_size: # (2)
                eatable_fish.append((dist, nr, nc))
                min_dist = min(dist, min_dist)
            elif not fish or fish == shark_size: # (3)
                q.append((dist, nr, nc))

    if eatable_fish:
        eatable_fish.sort() # (4)
        return eatable_fish[0]

    return (0, 0, 0)


def is_out_of_range(r, c):
    return r < 0 or r >= n or c < 0 or c >= n


n = int(stdin.readline())
sea = []
for i in range(n):
    fishes = list(map(int, stdin.readline().split()))
    for j in range(n):
        if fishes[j] == 9:
            shark_r, shark_c = i, j
            fishes[j] = 0
    sea.append(fishes)

sec, eat_cnt, shark_size = 0, 0, 2
direction = [1, 0, -1, 0]
while True:
    dist, shark_r, shark_c = bfs(shark_r, shark_c)
    if not dist: # (5)
        break

    sea[shark_r][shark_c] = 0
    eat_cnt += 1
    sec += dist # (6)
    if shark_size == eat_cnt:
        shark_size += 1
        eat_cnt = 0

print(sec)
```


* (1) 가장 가까운 물고기 거리보다 크면 탐색하지 않는다.
* (2) 먹을 수 있는 물고기일 경우 리스트에 저장하고 최소 거리를 갱신한다.
* (3) 빈 칸이거나 물고기가 상어의 크기와 같을 경우 큐에 삽입한다.
* (4) 거리, 행, 열을 비교하여 오름차순 정렬한다.
* (5) 먹을 수 있는 물고기가 없을 경우 탈출한다.
* (6) 이동 거리만큼 시간을 더한다.
