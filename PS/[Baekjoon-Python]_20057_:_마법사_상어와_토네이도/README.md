[Baekjoon-Python] 20057 : 마법사 상어와 토네이도
=
<https://www.acmicpc.net/problem/20057>


접근
--


1. 비율이 적힌 칸의 인덱스를 미리 계산한다.


![](https://blog.kakaocdn.net/dn/ccHaTk/btsDQU1RdgK/KCGXCeJ7xA8BTZqpvvyjmK/img.png)



2. 토네이도는 x번 전진을 두 번하면 x \+ 1번 전진한다.
3. y의 모래를 비율이 적힌 칸으로 모두 이동시킨 후에 남은 모래를 알파로 이동시킨다.


풀이
--



```python
from sys import stdin
from math import floor


def tornado(r, c, d):
    over_amount = 0
    sand, board[r][c] = board[r][c], 0
    dr, dc = direction[d]
    tmp = 0
    for i in range(9): # (1)
        pr, pc = p_direction[d][i]
        moved_sand = floor(sand * percent[i])
        if is_out_of_range(r + pr, c + pc): # (2)
            over_amount += moved_sand
        else:
            board[r + pr][c + pc] += moved_sand
        tmp += moved_sand

    sand -= tmp # (3)
    if is_out_of_range(r + dr, c + dc):
        over_amount += sand
    else:
        board[r + dr][c + dc] += sand

    return over_amount


def is_out_of_range(r, c):
    return r < 0 or r >= n or c < 0 or c >= n


n = int(stdin.readline())
board = [list(map(int, stdin.readline().split())) for _ in range(n)]

direction = [(0, -1), (1, 0), (0, 1), (-1, 0)]
percent = [0.01, 0.07, 0.02, 0.1, 0.05, 0.1, 0.07, 0.02, 0.01]
p_direction = [
    [(-1, 1), (-1, 0), (-2, 0), (-1, -1), (0, -2), (1, -1), (1, 0), (2, 0), (1, 1)],
    [(-1, -1), (0, -1), (0, -2), (1, -1), (2, 0), (1, 1), (0, 1), (0, 2), (-1, 1)],
    [(1, -1), (1, 0), (2, 0), (1, 1), (0, 2), (-1, 1), (-1, 0), (-2, 0), (-1, -1)],
    [(1, 1), (0, 1), (0, 2), (-1, 1), (-2, 0), (-1, -1), (0, -1), (0, -2), (1, -1)],
] # (4)
moved = [0] * n
d, cnt = 0, 1
r = c = n // 2 # (5)
res = 0
while r != 0 or c != 0:
    if moved[cnt] == 2 and cnt < n - 1: # (6)
        cnt += 1

    for _ in range(cnt):
        r += direction[d][0]
        c += direction[d][1]
        res += tornado(r, c, d)

    d = (d + 1) % 4
    moved[cnt] += 1

print(res)
```


* (1\) 모래 비율을 순회한다.
* (2\) 격자 밖으로 나간 모래의 양을 더한다.
* (3\) 알파에 해당하는 모래의 양이다.
* (4\) 이동 방향에 따라 y를 기준으로 모래 비율이 적힌 칸의 인덱스를 의미한다.  
 방향은 `0:좌, 1: 하, 2:우, 3:상`이다.
* (5\) 격자의 정중앙 인덱스로 초기화한다.
* (6\) cnt는 전진 횟수이다. 토네이도는 x번 전진을 두 번 하면 다음은 x \+ 1번 전진을 두 번한다. 마지막 토네이도의 전진만 세 번하기 때문에 `cnt < n - 1` 조건을 추가한다.  
![](https://blog.kakaocdn.net/dn/ZSuWc/btsDJZwxs74/e83tvMNCbKl3Wip3CLJGz0/img.png)
