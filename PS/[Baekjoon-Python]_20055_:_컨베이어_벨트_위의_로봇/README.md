[Baekjoon-Python] 20055 : 컨베이어 벨트 위의 로봇
=
<https://www.acmicpc.net/problem/20055>


접근
--


1. 벨트는 2N 길이의 큐, 로봇은 N길이의 큐로 사용한다.


풀이
--



```python
from sys import stdin
from collections import deque


def put_robot(idx):
    global durability

    robot[idx] = True
    belt[idx] -= 1
    if belt[idx] == 0:
        durability += 1


n, k = map(int, stdin.readline().split())
belt = deque(map(int, stdin.readline().split()))

robot = deque([False] * n)
step, durability = 0, 0
while durability < k:
    belt.rotate()
    robot.rotate()

    robot[0] = False # (1)
    robot[-1] = False # (2)
    for i in range(n - 2, -1, -1):
        if robot[i] and not robot[i + 1] and belt[i + 1] > 0: # (3)
            robot[i] = False
            put_robot(i + 1)

    if belt[0] > 0: # (4)
        put_robot(0)
    step += 1

print(step)
```


* (1) 회전하기 전 N - 1에 있는 로봇이 N으로 이동한 경우 회전하면 True인 상태로 0번 인덱스로 오기 떄문에 False 처리한다.
* (2) 벨트 회전 후 내리는 위치에 있는 로봇을 내린다.
* (3) 로봇을 한 칸 이동한다.
* (4) 올리는 위치에 내구도가 있으면 로봇을 올린다.
