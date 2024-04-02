[Baekjoon-Python] 19238 : 스타트 택시
=
<p><a href="https://www.acmicpc.net/problem/19238">https://www.acmicpc.net/problem/19238</a></p>
<h2>접근</h2>
<ol>
<li>bfs 탐색하여 택시 좌표에서 각각의 영역까지 거리를 구한다.</li>
<li>가장 가까운 승객 좌표를 찾는다.</li>
<li>bfs 탐색하여 승객 좌표에서 목적지까지의 거리를 구한다.</li>
<li>연료가 충분하면 택시의 좌표를 승객의 목적지로 변경한다.</li>
<li>택시 -> 승객 출발지 <strong>연료 감소</strong>, 승객 출발지 -> 승객 목적지 <strong>연료 감소</strong>, 목적지에 도착하면 출발지에서 목적지까지 소모한 연료의 두 배만큼 <strong>연료 증가</strong></li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin
from collections import deque


def bfs(start\_r, start\_c): # (1)
 visited = [[-1] \* n for \_ in range(n)]
 q = deque([(start\_r, start\_c)])
 visited[start\_r][start\_c] = 0

 while q:
 r, c = q.popleft()
 for i in range(4):
 nr, nc = r + direction[i], c + direction[3 - i]
 if is\_out\_of\_range(nr, nc) or visited[nr][nc] != -1:
 continue
 visited[nr][nc] = visited[r][c] + 1
 q.append((nr, nc))

 return visited


def find\_passenger(distances): # (2)
 for p in passengers:
 r, c = p[1:3]
 p[0] = distances[r - 1][c - 1]
 passengers.sort(reverse=True) # (3)
 return passengers.pop()


def is\_out\_of\_range(r, c):
 return r < 0 or r >= n or c < 0 or c >= n or board[r][c] == 1


n, m, fuel = map(int, stdin.readline().split())
board = [list(map(int, stdin.readline().split())) for \_ in range(n)]
tr, tc = map(int, stdin.readline().split())
passengers = []
for \_ in range(m):
 passengers.append([0] + list(map(int, stdin.readline().split()))) # (4)

direction = [1, 0, -1, 0]
for \_ in range(m):
 distances = bfs(tr - 1, tc - 1)
 dist, sr, sc, dr, dc = find\_passenger(distances)
 if dist == -1: # (5)
 fuel = -1
 break

 fuel -= dist # (6)
 if fuel <= 0: # (7)
 fuel = -1
 break

 distances = bfs(sr - 1, sc - 1) # (8)
 next\_dist = distances[dr - 1][dc - 1]
 if next\_dist == -1 or fuel < next\_dist:
 fuel = -1
 break

 fuel += next\_dist # (9)
 tr, tc = dr, dc # (10)

print(fuel)</code></pre>
<ul>
<li>(1) 택시 좌표에서 각각의 영역까지 거리를 구한다.</li>
<li>(2) 가장 가까운 승객을 찾는다.</li>
<li>(3) 거리를 기준으로 내림차순 정렬한다. 거리가 같으면 행, 행이 같으면 열을 기준으로 정렬하게 된다.</li>
<li>(4) 0번 인덱스는 거리를 저장한다.</li>
<li>(5) 가장 가까운 승객의 거리가 -1이면 태울 수 있는 승객이 없는 경우이므로 탈출한다.</li>
<li>(6) 태울 수 있는 승객이 있으면 승객과의 거리만큼 연료를 감소시킨다.</li>
<li>(7) 연료가 없으면 승객의 목적지로 이동할 수 없으므로 탈출한다.</li>
<li>(8) 승객의 출발지에서 목적지까지의 거리를 구한다.</li>
<li>(9) 승객의 출발지에서 목적지까지 이동할 때 연료를 감소시키지 않았기 때문에 한 번만 더해준다.</li>
<li>(10) 택시의 좌표를 이동한다.</li>
</ul>