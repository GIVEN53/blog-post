[Baekjoon-Python] 1520 : 내리막길
=
<https://www.acmicpc.net/problem/1520>


접근
--


* dfs 또는 bfs 탐색하여 높이가 더 낮은 경우만 이동한다.
* 중복 탐색을 방지하기 위해 지점에 방문한 횟수를 메모이제이션한다.


풀이1 - bfs
---------



```python
from sys import stdin
from heapq import heappop, heappush


def bfs():
    q = []
    heappush(q, (-board[0][0], 0, 0)) # (1)
    while q:
        h, x, y = heappop(q)
        h *= -1

        for i in range(4):
            nx = x + directions[i]
            ny = y + directions[3 - i]
            if nx < 0 or nx >= m or ny < 0 or ny >= n or h <= board[nx][ny]:
                continue

            if not dp[nx][ny]:
                heappush(q, (-board[nx][ny], nx, ny)) # (2)
            dp[nx][ny] += dp[x][y]

    return dp[m - 1][n - 1]


m, n = map(int, stdin.readline().split())
board = [[*map(int, stdin.readline().split())] for _ in range(m)]

directions = [1, 0, -1, 0]
dp = [[0] * n for _ in range(m)]
dp[0][0] = 1
print(bfs())
```


* (1) 높이를 음수로 삽입해서 최대 힙으로 사용한다.
* (2) 아직 방문하지 않은 지점일 때만 힙에 삽입한다.
> 20으로 가는 경로가 두 개 있으면 아래와 같이 삽입, 삭제가 발생한다.  
> ![](https://blog.kakaocdn.net/dn/dfM887/btsDz8lsqH1/RDadkWJn5Dup2RfQyoGH61/img.png)  
> ![](https://blog.kakaocdn.net/dn/mg1AH/btsDxzqxFSt/KurahcjlTDj1juh7Kyp04k/img.png)  
> ![](https://blog.kakaocdn.net/dn/beO3p6/btsDAuaGpXG/TAtFXaaMmydI7kViEXKnfK/img.png)  
> ![](https://blog.kakaocdn.net/dn/QMiSW/btsDBBtDbWJ/aKgFTFd199qMxfrvxlRFn0/img.png)
> 
> 
> 
> 
>


풀이2 - dfs
---------



```python
from sys import stdin


def dfs(x, y):
    if x == m - 1 and y == n - 1:
        return 1

    if dp[x][y] != -1: # (1)
        return dp[x][y]

    dp[x][y] = 0
    for i in range(4):
        nx = x + directions[i]
        ny = y + directions[3 - i]
        if nx < 0 or nx >= m or ny < 0 or ny >= n or board[x][y] <= board[nx][ny]:
            continue

        dp[x][y] += dfs(nx, ny)

    return dp[x][y]


m, n = map(int, stdin.readline().split())
board = [[*map(int, stdin.readline().split())] for _ in range(m)]

directions = [1, 0, -1, 0]
dp = [[-1] * n for _ in range(m)]
print(dfs(0, 0))
```


* (1) 제일 오른쪽 아래 칸에 도달하지 못한 경로도 존재하기 때문에 -1로 초기화하여 방문 여부를 판단한다.
