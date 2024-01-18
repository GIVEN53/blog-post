[Baekjoon-Python] 16234 : 인구 이동
=
<https://www.acmicpc.net/problem/16234>


접근
--


1. 각 좌표마다 bfs 탐색하여 국경선을 열 수 있는 인접 국가 좌표를 구한다.
2. 국경선을 연 국가들은 인구 수의 평균을 저장한다.
3. 이전 날짜에 국경선을 연 국가만 다시 탐색하여 중복 탐색을 제거한다. 이전 날짜에 국경선을 열지 않은 국가여도 국경선을 연 국가와 인접해 있으면 현재 날짜에 다시 국경선을 열 수 있다.


풀이
--



```python
from sys import stdin
from collections import deque


def bfs(r, c):
    q = deque([(r, c)])
    opened = [(r, c)]
    tot = country[r][c]
    while q:
        r, c = q.popleft()

        for i in range(4):
            nr, nc = r + direction[i], c + direction[3 - i]
            if is_out_of_range(nr, nc) or visited[nr][nc] == day:
                continue

            if is_within_population(r, c, nr, nc):
                visited[nr][nc] = day
                tot += country[nr][nc]
                q.append((nr, nc))
                opened.append((nr, nc))

    if len(opened) > 1:
        move(opened, tot)


def is_out_of_range(r, c):
    return r < 0 or r >= N or c < 0 or c >= N


def is_within_population(r, c, nr, nc):
    return L <= abs(country[r][c] - country[nr][nc]) <= R # (1)


def move(opened, tot):
    avg = tot // len(opened)
    for r, c in opened:
        country[r][c] = avg
        candidate.append((r, c)) # (2)


N, L, R = map(int, stdin.readline().split())
country = [list(map(int, stdin.readline().split())) for _ in range(N)]

candidate = deque([(i, j) for i in range(N) for j in range(i % 2, N, 2)]) # (3)
visited = [[-1] * N for _ in range(N)]
direction = [1, 0, -1, 0]
day = 0
while candidate:
    for _ in range(len(candidate)): # (4)
        r, c = candidate.popleft()
        if visited[r][c] == day:
            continue
        visited[r][c] = day # (5)
        bfs(r, c)

    day += 1

print(day - 1)
```


* (1) 두 국가의 인구 차이가 L과 R 사이인지 확인한다.
* (2) 국경을 연 국가만 다시 후보 국가에 추가하여 중복 탐색을 제거한다.
* (3) 상하좌우가 겹치지 않도록 체스판처럼 좌표를 저장하여 중복 탐색을 제거한다.
* (4) 현재 날짜의 후보 국가만 큐에서 꺼내 탐색한다.
* (5) 현재 날짜로 방문 처리한다.
