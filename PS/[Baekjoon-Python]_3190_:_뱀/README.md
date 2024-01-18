[Baekjoon-Python] 3190 : 뱀
=
<https://www.acmicpc.net/problem/3190>


접근
--


1. 큐를 뱀으로 사용한다.


풀이
--



```python
from sys import stdin
from collections import deque


def is_out_of_range(r, c):
    return r < 0 or r >= n or c < 0 or c >= n


def turn_direction(moving, i):
    if moving == 'L':
        return (i + 3) % 4
    else:
        return (i + 1) % 4


n, k = int(stdin.readline()), int(stdin.readline())
board = [[0] * n for _ in range(n)]
for _ in range(k):
    r, c = map(int, stdin.readline().split())
    board[r - 1][c - 1] = 1 # (1)

L = int(stdin.readline())
moves = deque(stdin.readline().split() for _ in range(L))

r = c = 0
snake = deque([(r, c)])
direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
d = 1 # (2)
second = 0
while True:
    second += 1
    r, c = r + direction[d][0], c + direction[d][1]
    if is_out_of_range(r, c) or (r, c) in snake: # (3)
        break

    snake.append((r, c))
    if board[r][c] == 1:
        board[r][c] = 0
    else:
        snake.popleft()

    if moves and second == int(moves[0][0]): # (4)
        d = turn_direction(moves[0][1], d)
        moves.popleft()

print(second)
```


* (1) 사과를 1로 저장한다.
* (2) direction은 순서대로 상, 우, 하, 좌의 좌표이다. 뱀은 처음에 오른쪽을 향하기 때문에 오른쪽 인덱스부터 시작한다.
* (3) 범위를 벗어났거나 몸에 부딪히면 종료한다.
* (4) 현재 초가 끝난 뒤에 방향 정보가 있으면 회전한다.
