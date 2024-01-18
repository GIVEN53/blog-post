[Baekjoon-Python] 14503 : 로봇 청소기
=
<https://www.acmicpc.net/problem/14503>


접근
--


1. 청소한 칸을 청소하지 않은 칸, 벽과 구분하기 위해 2로 저장한다.


풀이
--



```python
from sys import stdin

n, m = map(int, stdin.readline().split())
r, c, d = map(int, stdin.readline().split())
room = [stdin.readline().split() for _ in range(n)]

direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
cleaning_cnt = 1
while True:
    room[r][c] = '2'
    for _ in range(4):
        d = (d + 3) % 4
        nr, nc = r + direction[d][0], c + direction[d][1]
        if room[nr][nc] == '0': # (1)
            r, c = nr, nc 
            cleaning_cnt += 1
            break

    else: # (2)
        r, c = r + direction[d][0] * -1, c + direction[d][1] * -1
        if room[r][c] == '1':
            break

print(cleaning_cnt)
```


* (1) 상하좌우 중 청소되지 않은 칸이 있으면 전진한다.
* (2) 상하좌우 중 청소되지 않은 칸이 없으면 뒤로 한 칸 후진하고 벽이면 종료한다.
