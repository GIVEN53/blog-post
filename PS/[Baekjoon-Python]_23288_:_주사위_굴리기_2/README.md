[Baekjoon-Python] 23288 : 주사위 굴리기 2
=
<p><a href="https://www.acmicpc.net/problem/23288">https://www.acmicpc.net/problem/23288</a></p>
<h2>접근</h2>
<ol>
<li>지도를 bfs 탐색하여 연속해서 이동할 수 있는 좌표를 구한 후 점수를 미리 계산해서 중복을 제거한다.</li>
<li>주사위의 인덱스를 <code>0:top, 1:north, 2:east, 3:west, 4:south, 5:bottom</code>으로 두고 굴리는 방향에 따라 주사위 면을 재구성한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin
from collections import deque


def bfs(r, c) -> set: # (1)
 q = deque([(r, c)])
 same\_scores = {(r, c)}
 while q:
 r, c = q.popleft()
 for d in direction:
 nr, nc = r + d[0], c + d[1]
 if is\_out\_of\_range(nr, nc) or (nr, nc) in same\_scores:
 continue
 if board[nr][nc] == board[r][c]:
 q.append((nr, nc))
 same\_scores.add((nr, nc)) 

 return same\_scores


def roll(dice, d) -> list: # (2)
 top, north, east, west, south, bottom = dice
 if d == 0:
 return [south, top, east, west, bottom, north]
 elif d == 1:
 return [west, north, top, bottom, south, east]
 elif d == 2:
 return [north, bottom, east, west, top, south]
 else:
 return [east, north, bottom, top, south, west]


def move(r, c, d): # (3)
 nr, nc = r + direction[d][0], c + direction[d][1]
 if is\_out\_of\_range(nr, nc): # (4)
 d = (d + 2) % 4
 r += direction[d][0]
 c += direction[d][1]

 return r, c, d


def is\_out\_of\_range(r, c) -> bool:
 return r < 0 or r >= n or c < 0 or c >= m


def rotate\_direction(bottom, space, d) -> int: # (5)
 if bottom > space:
 d = (d + 1) % 4
 elif bottom < space:
 d = (d - 1) % 4

 return d


n, m, k = map(int, stdin.readline().split())
board = [list(map(int, stdin.readline().split())) for \_ in range(n)]

scores = [[0] \* m for \_ in range(n)]
direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
for r in range(n):
 for c in range(m):
 if scores[r][c] == 0:
 same\_scores = bfs(r, c)
 score = len(same\_scores) \* board[r][c] # (6)
 for sr, sc in same\_scores:
 scores[sr][sc] = score

dice = [1, 2, 3, 4, 5, 6]
r, c, d = 0, 0, 1
result = 0
while k:
 r, c, d = move(r, c, d)
 dice = roll(dice, d)
 result += scores[r][c]
 d = rotate\_direction(dice[-1], board[r][c], d)
 k -= 1

print(result)</code></pre>
<ul>
<li>(1) <code>(r, c)</code> 좌표에서 연속해서 이동할 수 있는 좌표를 모두 구한다.</li>
<li>(2) 주사위를 굴리는 방향에 맞춰서 주사위 면을 재구성한다.</li>
<li>(3) 주사위를 이동한다.</li>
<li>(4) 범위를 벗어났을 경우 방향을 반대로 바꾼다.</li>
<li>(5) 주사위 바닥면의 정수와 칸에 있는 정수를 비교하여 방향을 변경한다.</li>
<li>(6) <code>이동할 수 있는 칸의 수 \* 좌표의 정수</code>로 점수를 구하고 연속해서 이동할 수 있는 모든 좌표에 점수를 저장한다.</li>
</ul>