[Baekjoon-Python] 14500 : 테트로미노
=
<https://www.acmicpc.net/problem/14500>


접근
--


1. 모든 좌표에서 dfs 탐색해서 테트로미노를 구한다.
2. 폴리오미노가 2개일 때 3번째 폴리오미노를 더하고 2번째 좌표에서 다시 탐색해서 `ㅗ, ㅏ, ㅓ, ㅜ` 테트로미노를 구한다.


풀이
--



```python
from sys import stdin


def dfs(depth, total, r, c):
    global res

    if res >= total + (4 - depth) * max_num: # (1)
        return

    if depth == 4: # (2)
        res = max(res, total)
        return

    for i in range(4):
        nr, nc = r + direction[i], c + direction[3 - i]
        if is_out_of_range(nr, nc) or visited[nr][nc]:
            continue
        if depth == 2: # (3)
            visited[nr][nc] = True
            dfs(depth + 1, total + board[nr][nc], r, c)
            visited[nr][nc] = False

        visited[nr][nc] = True
        dfs(depth + 1, total + board[nr][nc], nr, nc)
        visited[nr][nc] = False


def is_out_of_range(r, c):
    return r < 0 or r >= n or c < 0 or c >= m


n, m = map(int, stdin.readline().split())
board = [list(map(int, stdin.readline().split())) for _ in range(n)]

visited = [[False] * m for _ in range(n)]
direction = [1, 0, -1, 0]
res = 0
max_num = max(map(max, board))
for r in range(n):
    for c in range(m):
        visited[r][c] = True
        dfs(1, board[r][c], r, c)
        visited[r][c] = False

print(res)
```


* (1) 남은 폴리오미노를 board의 가장 큰 값에 놓아도 최댓값을 갱신할 수 없을 경우 백트래킹한다.
* (2) 폴리오미노 4개를 모두 탐색했을 경우 최댓값을 갱신한다.
* (3) 현재 폴리오미노가 2개일 때 3번째 폴리오미노를 더한 상태에서 r, c 좌표로 다시 dfs 탐색한다.  
예를 들어 `◻︎◻︎` 상태에서 3번째 폴리오미노를 더해 `◻︎◻︎◻︎`가 되면 `◻︎◼︎◻︎`의 색칠된 폴리오미노에서 다음 폴리오미노를 탐색한다. 이 때는 `ㅗ, ㅜ` 테트로미노를 찾을 수 있게 된다.
