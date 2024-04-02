[Baekjoon-Python] 4179 : 불!
=
<p><a href="https://www.acmicpc.net/problem/4179">https://www.acmicpc.net/problem/4179</a></p>
<h2>접근</h2>
<ol>
<li>불과 지훈 좌표를 따로 저장한다.</li>
<li>해당 분동안 불을 먼저 bfs로 확산한 후 지훈을 bfs 탐색한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin
from collections import deque


def escape():
 maze[jihoon[0][0]][jihoon[0][1]] = -1
 minutes = 0
 while jihoon:
 minutes += 1
 spread\_fire()
 for \_ in range(len(jihoon)): # (1)
 r, c = jihoon.popleft()
 for i in range(4):
 nr, nc = r + direction[i], c + direction[3 - i]
 if is\_out\_of\_range(nr, nc): # (2)
 return minutes
 if is\_not\_space(nr, nc) or maze[nr][nc] == -1: # (3)
 continue
 maze[nr][nc] = -1
 jihoon.append((nr, nc))
 return "IMPOSSIBLE"


def spread\_fire():
 for \_ in range(len(fire)): # (4)
 r, c = fire.popleft()
 for i in range(4):
 nr, nc = r + direction[i], c + direction[3 - i]
 if is\_out\_of\_range(nr, nc) or is\_not\_space(nr, nc):
 continue
 maze[nr][nc] = "F"
 fire.append((nr, nc))


def is\_not\_space(r, c):
 return maze[r][c] == "#" or maze[r][c] == "F"


def is\_out\_of\_range(r, c):
 return r < 0 or r >= R or c < 0 or c >= C


R, C = map(int, stdin.readline().split())
maze = []
jihoon = deque()
fire = deque()
for r in range(R):
 m = list(stdin.readline().rstrip())
 for c in range(C):
 if m[c] == "F":
 fire.append((r, c)) # (5)
 elif m[c] == "J":
 jihoon.append((r, c)) # (6)
 maze.append(m)

direction = [1, 0, -1, 0]
print(escape())</code></pre>
<ul>
<li>(1) 현재 분에 큐에 존재하는 지훈 좌표만 탐색한다. 이동한 지훈 좌표는 다음 분에 탐색한다.</li>
<li>(2) 범위를 벗어났을 경우 미로를 탈출하므로 현재 분을 리턴한다.</li>
<li>(3) 벽 또는 불이거나 이미 방문한 위치일 경우 건너뛴다.</li>
<li>(4) 현재 분에 큐에 존재하는 불 좌표만 탐색한다. 확산된 불은 다음 분에 탐색한다.</li>
<li>(5) 불 좌표를 저장한다.</li>
<li>(6) 지훈 좌표를 저장한다.</li>
</ul>