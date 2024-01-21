[Baekjoon-Python] 17825 : 주사위 윷놀이
=
<https://www.acmicpc.net/problem/17825>


접근
--


1. 게임판을 아래와 같이 설정한다.  
![](https://blog.kakaocdn.net/dn/lXzma/btsDJTV3y90/3B6xRuLCGk7mvxtg60kcvK/img.png)
2. `r = 0`: **10, 20, 30에 말이 놓이지 않았을 때** 이동하는 칸이다.  
![](https://blog.kakaocdn.net/dn/IaNCM/btsDI80wjEG/Dh33kKFvNbwutSKqVylZSk/img.png)
3. `r = 1`: `r = 0`에서 **10에 말이 놓였을 때** 이동하는 칸이다.  
![](https://blog.kakaocdn.net/dn/J2uHc/btsDIBuRxRq/eSJCqS22kYnQDS3djSpd60/img.png)
4. `r = 2`: `r = 0`에서 **20에 말이 놓였을 때** 이동하는 칸이다.  
![](https://blog.kakaocdn.net/dn/bw6NBl/btsDGLrfD46/dVfZbGU6Xr5XnAXh9B89J1/img.png)
5. `r = 3`: `r = 0`에서 **30에 말이 놓였을 때** 이동하는 칸이다.  
![](https://blog.kakaocdn.net/dn/JpUuv/btsDItKGAlt/GNPfuShuW0yBN6tbkMWnu1/img.png)
6. `r = 4`: `r = 0, 1, 2, 3, 5`에서 **40에 말이 놓였을 때** 이동하는 칸이다.
7. `r = 5`: `r = 1, 2, 3`에서 **25, 30, 35에 말이 놓였을 때** 이동하는 칸이다.
8. 말이 이동한 좌표에 따라 게임판의 인덱스를 조정하고 dfs 탐색한다.


풀이
--



```python
from sys import stdin


def dfs(i, record):
    global max_record

    if i == 10:
        max_record = max(max_record, record) # (1)
        return
    elif record + 40 * (10 - i) < max_record: # (2)
        return

    now_dice = dices[i]
    for k in range(4):
        if arrived[k]:
            continue

        tmp = [players[k][0], players[k][1]]
        r, c = players[k][0], players[k][1] + now_dice # (3)
        if len(board[r]) - 1 < c: # (4)
            players[k][0], players[k][1] = r, c
            arrived[k] = True
            dfs(i + 1, record)
            arrived[k] = False
            players[k][0], players[k][1] = tmp
            continue

        if board[r][c] == 40: # (5)
            r, c = 4, 0
        elif r == 0 and board[r][c] % 10 == 0: # (6)
            r, c = board[r][c] // 10, 0
        elif 0 < r < 4 and board[r][c] % 5 == 0: # (7)
            r, c = 5, board[r][c] // 5 - 5

        if [r, c] not in players: # (8)
            players[k][0], players[k][1] = r, c
            dfs(i + 1, record + board[r][c])
            players[k][0], players[k][1] = tmp


board = [[i for i in range(0, 41, 2)]]
board.append([10, 13, 16, 19, 25, 30, 35, 40])
board.append([20, 22, 24, 25, 30, 35, 40])
board.append([30, 28, 27, 26, 25, 30, 35, 40])
board.append([40])
board.append([25, 30, 35, 40])

dices = list(map(int, stdin.readline().split()))
players = [[0, 0] for _ in range(4)]
arrived = [False] * 4
max_record = 0
dfs(0, 0)

print(max_record)
```


* (1) 주사위를 모두 굴렸으면 점수의 최댓값을 갱신한다.
* (2) 남은 주사위 횟수를 모두 굴렸을 때 전부 40점이어도 최댓값보다 작을 경우 백트래킹한다.
* (3) 주사위 수만큼 전진한다.
* (4) 말이 도착했을 경우 도착 여부를 체크하고, 도착한 말은 점수가 없으므로 추가되는 점수 없이 dfs 탐색한다.
* (5) 말이 위치한 칸의 숫자가 40일 경우 board의 `(4, 0)`으로 말을 이동한다.
* (6) 말의 `r == 0`이고 게임판 점수가 10의 배수(10, 20, 30)일 경우 board의 `(점수 / 10 , 0)`으로 말을 이동한다.
* (7) 말의 `r == 1 or 2 or 3`이고 점수가 5의 배수(25, 30, 35)일 경우 board의 `(5, 점수 / 5 - 5)`으로 말을 이동한다.
* (8) 이동한 칸에 다른 말이 없을 경우 점수를 추가하고 dfs 탐색한다.
