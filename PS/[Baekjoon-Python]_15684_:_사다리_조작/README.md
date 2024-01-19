[Baekjoon-Python] 15684 : 사다리 조작
=
<https://www.acmicpc.net/problem/15684>


접근
--


1. 각각의 세로선마다 놓여진 가로선 개수가 홀수이면 원래 세로선으로 돌아올 수 없다. 즉, 세로선마다 놓여진 가로선 개수가 모두 짝수여야 한다.
2. 세로선을 dfs 탐색해서 가로선이 놓여있지 않으면 가로선을 추가한다.
3. 추가한 가로선 개수가 3개보다 많아질 경우 백트래킹한다.


풀이
--



```python
from sys import stdin


def is_same_vertical(): # (1)
    for j in range(1, n + 1):
        start = j
        for i in range(1, h + 1):
            if ladder[i][j]:
                j = ladder[i][j]

        if start != j:
            return False
    return True


def dfs(cnt, depth, now):
    global res

    if is_same_vertical(): # (2)
        res = min(res, cnt)
        return
    elif cnt == 3 or cnt >= res: # (3)
        return

    odd = 0
    for i in range(2, n + 1): # (4)
        if line[i] % 2:
            odd += 1
    if odd > 3 - cnt: # (5)
        return

    for i in range(depth, h + 1): # (6)
        k = now if depth == i else 1

        for j in range(k, n):
            if not ladder[i][j] and not ladder[i][j + 1]:
                ladder[i][j], ladder[i][j + 1] = j + 1, j
                line[j + 1] += 1
                dfs(cnt + 1, i, j + 2) # (7)
                ladder[i][j], ladder[i][j + 1] = 0, 0 # (8)
                line[j + 1] -= 1


n, m, h = map(int, stdin.readline().split())
ladder = [[0] * (n + 1) for _ in range(h + 1)]
line = [0] * (n + 1)
for _ in range(m):
    a, b = map(int, stdin.readline().split())
    ladder[a][b] = b + 1
    ladder[a][b + 1] = b
    line[b + 1] += 1

res = 4
dfs(0, 1, 1)
print(res if res < 4 else -1)
```


* (1) 사다리를 타고 내려가면서 출발 세로선과 도착 세로선이 같은지 확인한다.
* (2) (1)의 결과가 True일 때 최솟값을 갱신한다.
* (3) 정답은 최대 3까지다. 따라서 현재 가로선을 3개 추가했는데 첫 if문에 걸리지 않거나 추가한 가로선 개수가 최솟값보다 클 경우 백트래킹한다.
* (4) i번째 세로선에 놓인 가로선의 개수가 홀수인 세로선의 개수를 구한다.
* (5) 가로선의 개수가 홀수인 세로선의 개수가 추가로 더 놓을 수 있는 가로선 개수보다 크면 4개 이상의 가로선을 추가해야 함을 의미한다. 따라서 백트래킹해서 더 이상 탐색하지 않는다.
* (6) 가로로 순회한다. 세로로 dfs 탐색하기 때문에 다음 가로를 순회하면 1번째 세로선부터 다시 순회한다.
* (7) `j, j + 1` 세로선 사이와 `j + 1, j + 2` 세로선 사이에 가로선이 없을 때 가로선을 추가하고 dfs 탐색한다. `j, j + 1` 세로선 사이에 가로선을 추가하면 `j + 1, j + 2` 세로선 사이에 연속으로 가로선을 놓을 수 없기 때문에 `j + 2` 세로선을 탐색한다.
* (8) 모든 경우의 수를 확인해야 하기 때문에 놓았던 가로선을 제거한다.
