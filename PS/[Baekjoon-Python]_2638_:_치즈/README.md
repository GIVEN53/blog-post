[Baekjoon-Python] 2638 : 치즈
=
<https://www.acmicpc.net/problem/2638>


접근
--


1. bfs 탐색해서 공기와 접촉한 치즈를 찾는다. 탐색된 공기, 치즈는 방문 처리해서 중복 탐색을 방지한다.
2. 공기와 접촉한 치즈 중 두 변 이상이 접촉한 치즈를 필터링한다.
3. 필터링되지 않은 치즈는 다시 bfs 탐색하기 위해 방문 처리를 해제한다.
4. 필터링된 치즈를 녹인다.
5. 녹인 치즈부터 bfs 탐색하여 치즈가 없어질 때까지 반복한다.


풀이
--



```python
from sys import stdin
from collections import deque


def bfs(q):
    cheese = []
    while q:
        x, y = q.popleft()

        for i in range(4):
            nx = x + directions[i]
            ny = y + directions[3 - i]
            if is_out_of_range(nx, ny) or visited[nx][ny]:
                continue

            visited[nx][ny] = True
            if board[nx][ny]: # (1)
                cheese.append((nx, ny))
            else:
                q.append((nx, ny))

    return cheese


def is_out_of_range(x, y):
    return x < 0 or x >= n or y < 0 or y >= m


def melt(cheese):
    melting_cheese = []
    for x, y in cheese:
        cnt = 0
        for i in range(4):
            nx = x + directions[i]
            ny = y + directions[3 - i]
            if is_out_of_range(nx, ny) or not visited[nx][ny] or board[nx][ny]: # (2)
                continue
            cnt += 1

        if cnt >= 2:
            melting_cheese.append((x, y))
        else:
            visited[x][y] = False

    for x, y in melting_cheese: # (3)
        board[x][y] = 0

    return melting_cheese


n, m = map(int, stdin.readline().split())
board = [[*map(int, stdin.readline().split())] for _ in range(n)]
visited = [[False] * m for _ in range(n)]

directions = [1, 0, -1, 0]
hours = 0
q = deque([(0, 0)])
while True:
    cheese = bfs(q)
    if not cheese:
        break

    melting_cheese = melt(cheese)
    q = deque(melting_cheese) # (4)
    hours += 1

print(hours)
```


* (1) 치즈는 치즈 리스트에 저장하고 외부 공기만 다시 큐에 넣어서 표면의 치즈만 탐색하도록 한다.
* (2) 치즈의 상하좌우를 확인할 때 외부 공기만 카운트되어야 한다. 방문 처리되지 않은 것은 내부 공기 또는 공기와 접촉하지 않은 치즈이고, 방문했지만 치즈인 것은 공기와 접촉한 다른 치즈이다.
* (3) 녹일 치즈를 찾고 바로 녹이면 공기와 한 변만 접촉해 있던 다른 치즈가 녹을 수 있다. 따라서 녹일 치즈들을 리스트에 저장하고 한 번에 녹인다.
* (4) 이미 탐색한 외부 공기는 방문 처리했기 때문에 녹인 치즈부터 bfs 탐색해서 탐색 범위를 좁힌다.
