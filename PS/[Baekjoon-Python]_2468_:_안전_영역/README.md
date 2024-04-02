[Baekjoon-Python] 2468 : 안전 영역
=
<p><a href="https://www.acmicpc.net/problem/2468">https://www.acmicpc.net/problem/2468</a></p>
<h2>접근</h2>
<ol>
<li>비의 양을 <code>0 ~ 지역의 최고 높이 - 1</code>까지 순회하면서 안전한 영역의 개수를 구한다.</li>
<li>안전한 영역은 bfs 탐색한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin
from collections import deque


def bfs(r, c, rain, q: deque):
 q.append((r, c))

 while q:
 r, c = q.popleft()
 for i in range(4):
 nr, nc = r + direction[i], c + direction[3 - i]
 if is\_out\_of\_range(nr, nc) or visited[nr][nc] or city[nr][nc] <= rain: # (1)
 continue
 visited[nr][nc] = True
 q.append((nr, nc))


def is\_out\_of\_range(r, c):
 return r < 0 or r >= n or c < 0 or c >= n


n = int(stdin.readline())
max\_height = 0
city = []
for \_ in range(n):
 c = list(map(int, stdin.readline().split()))
 max\_height = max(max\_height, max(c)) # (2)
 city.append(c)

direction = [1, 0, -1, 0]
q = deque()
res = 0
for rain in range(max\_height):
 visited = [[False] \* n for \_ in range(n)]
 area = 0
 for r in range(n):
 for c in range(n):
 if not visited[r][c] and city[r][c] > rain: # (3)
 visited[r][c] = True
 bfs(r, c, rain, q)
 area += 1
 res = max(res, area)

print(res)</code></pre>
<ul>
<li>(1) 범위를 벗어났거나 방문했거나 물에 잠긴 지역일 경우 건너뛴다.</li>
<li>(2) 지역의 최고 높이를 갱신한다.</li>
<li>(3) 방문하지 않았고 물에 잠기지 않은 지역일 때 안전한 영역을 bfs 탐색한다.</li>
</ul>