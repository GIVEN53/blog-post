[Baekjoon-Python] 17837 : 새로운 게임 2
=
<https://www.acmicpc.net/problem/17837>


접근
--


1. 턴마다 1번 말부터 순서대로 이동한다.
2. 체스판 한 칸에 여러 말이 존재할 수 있기 때문에 리스트를 사용한다.
3. 말을 위에서부터 꺼내면 뒤집한 상태가 된다. 다음 칸이 흰색이면 다시 뒤집고 빨간색이면 뒤집지 않는다.


풀이
--



```python
from sys import stdin


def move():
    direction = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    turn_cnt = 1
    while turn_cnt < 1001:
        for i in range(k):
            r, c, d = pieces[i]
            nr, nc = r + direction[d][0], c + direction[d][1]

            if is_out_of_range(nr, nc) or color[nr][nc] == "2": # (1)
                d = d + 1 if d % 2 == 0 else d - 1
                nr, nc = r + direction[d][0], c + direction[d][1]
                pieces[i][2] = d 
                if is_out_of_range(nr, nc) or color[nr][nc] == "2": # (2)
                    continue

            tmp = []
            while board[r][c][-1] != i: # (3)
                tmp.append(board[r][c].pop())
            tmp.append(board[r][c].pop())

            if color[nr][nc] == "0": # (4)
                tmp.reverse()

            board[nr][nc].extend(tmp) # (5)
            for j in tmp:
                pieces[j][0], pieces[j][1] = nr, nc

            if len(board[nr][nc]) >= 4: # (6)
                return turn_cnt
        turn_cnt += 1

    return -1 # (7)


def is_out_of_range(r, c):
    return r < 0 or r >= n or c < 0 or c >= n


n, k = map(int, stdin.readline().split())
color = [stdin.readline().split() for _ in range(n)]
board = [[[] for _ in range(n)] for _ in range(n)]
pieces = [None] * k
for i in range(k):
    r, c, d = map(int, stdin.readline().split())
    pieces[i] = [r - 1, c - 1, d - 1]
    board[r - 1][c - 1].append(i)

print(move())
```


* (1) 체스판을 벗어났거나 파란색 칸일 경우 반대 방향으로 변경한다.
* (2) 방향을 반대로 바꾼 후에 이동하려는 칸이 체스판을 벗어났거나 파란색 칸일 경우 이동하지 않는다.
* (3) i번 말까지 꺼낸다.
* (4) 역순으로 말을 꺼냈기 때문에 이동할 좌표가 흰색이면 뒤집는다.
* (5) 이동할 좌표에 말을 추가한다.
* (6) 이동한 좌표에 말이 4개 이상일 경우 턴 번호를 리턴한다.
* (7) 턴 번호가 1,000보다 클 경우 -1을 리턴한다.
