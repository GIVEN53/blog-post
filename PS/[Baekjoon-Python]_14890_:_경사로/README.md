[Baekjoon-Python] 14890 : 경사로
=
<https://www.acmicpc.net/problem/14890>


접근
--


1. 행과 열을 구분하여 두 번 순회한다.
2. 높이 차이가 2 이상이면 경사로를 놓을 수 없다.
3. 경사로를 놓았을 때 방문 처리하여 경사로가 겹치는 경우를 확인한다.


풀이
--



```python
from sys import stdin


def can_move(road):
    slope = [False] * N

    i = 1
    while i < N:
        if abs(road[i - 1] - road[i]) > 1: # (1)
            return False

        if road[i - 1] > road[i]: # (2)
            for j in range(i, i + L):
                if j >= N or road[j] != road[i]:
                    return False
                slope[j] = True
            i += L
        elif road[i - 1] < road[i]: # (3)
            if slope[i - L]: # (4)
                return False
            for j in range(i - L, i - 1):
                if j < 0 or road[j] != road[i - 1]:
                    return False
            i += 1
        else:
            i += 1

    return True


N, L = map(int, stdin.readline().split())
row_board = [list(map(int, stdin.readline().split())) for _ in range(N)]
col_board = list(zip(*row_board))

cnt = 0
for i in range(N):
    if can_move(row_board[i]):
        cnt += 1
    if can_move(col_board[i]):
        cnt += 1

print(cnt)
```


* (1) 전 칸 높이와 현재 칸 높이의 차이가 2 이상일 경우 경사로를 놓을 수 없다.
* (2) 전 칸 높이가 현재 칸보다 클 경우 현재 칸부터 앞으로 경사로를 놓을 수 있는지 확인한다.
* (3) 전 칸 높이가 현재 칸보다 작을 경우 전 칸부터 뒤로 경사로를 놓을 수 있는지 확인한다.
* (4) 놓을 경사로 범위에 이미 경사로가 놓아져 있을 경우 경사로를 놓을 수 없다.
