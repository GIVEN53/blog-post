[Baekjoon-Python] 14891 : 톱니바퀴
=
<https://www.acmicpc.net/problem/14891>


접근
--


1. 톱니바퀴를 데큐로 사용하여 회전하는 방향에 따라 삽입, 삭제한다.
2. 톱니바퀴의 인덱스를 `0:12시, 2:3시, 4:6시, 6:9시` 두고 회전시킨 톱니바퀴부터 dfs 탐색한다.
3. 톱니바퀴를 바로 회전시키면 조건을 만족하지 않는 톱니바퀴에 영향을 미치기 때문에 조건을 만족하는 톱니바퀴를 전부 찾은 후 한 번에 회전시킨다.
4. 현재 톱니바퀴의 6번 인덱스가 오른쪽 톱니바퀴의 2번 인덱스와 같지 않으면 오른쪽 톱니바퀴를 반대 방향으로 회전시킨다.
5. 현재 톱니바퀴의 2번 인덱스가 왼쪽 톱니바퀴의 6번 인덱스와 같지 않으면 왼쪽 톱니바퀴를 반대 방향으로 회전시킨다.
6. k번 회전시킨 후 0번 인덱스가 S극이면 톱니바퀴 번호만큼 1을 왼쪽으로 shift해서 더한다.


풀이
--



```python
from sys import stdin
from collections import deque


def dfs(now, d):
    if visited[now] == cnt:
        return

    visited[now] = cnt
    if now - 1 >= 0 and gears[now][6] != gears[now - 1][2]:
        dfs(now - 1, d * -1)

    if now + 1 < 4 and gears[now][2] != gears[now + 1][6]:
        dfs(now + 1, d * -1)

    if d == 1:
        gears[now].appendleft(gears[now].pop()) # (1)
    else:
        gears[now].append(gears[now].popleft()) # (2)


gears = [deque(stdin.readline().rstrip()) for _ in range(4)]
k = int(stdin.readline())

visited = [-1] * 4
cnt = 0
while cnt < k:
    now, d = map(int, stdin.readline().split())
    dfs(now - 1, d)
    cnt += 1

print(sum(1 << i if gears[i][0] == '1' else 0 for i in range(4))) # (3)
```


* (1) 시계 방향으로 회전한다.
* (2) 반시계 방향으로 회전한다.
* (3) 0번 인덱스가 S극이면 톱니바퀴 번호만큼 1을 왼쪽으로 shift해서 더한다.
