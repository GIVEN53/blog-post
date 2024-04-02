[Baekjoon-Python] 2178 : 미로 탐색
=
<p><a href="https://www.acmicpc.net/problem/2178">https://www.acmicpc.net/problem/2178</a></p>
<h2>접근</h2>
<ol>
<li>미로를 bfs 탐색한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin
from collections import deque


def bfs(x, y):
 q = deque([(x, y, maze[x][y])])

 while q:
 r, c, cnt = q.popleft()
 cnt += 1
 for i in range(4):
 nr, nc = r + direction[i], c + direction[3 - i]
 if is\_out\_of\_range(nr, nc):
 continue
 if maze[nr][nc] == 0 or maze[nr][nc] > cnt: # (1)
 maze[nr][nc] = cnt
 q.append((nr, nc, cnt))


def is\_out\_of\_range(r, c):
 return r < 0 or r >= n or c < 0 or c >= m or arr[r][c] == "0"


n, m = map(int, stdin.readline().split())
arr = [stdin.readline().rstrip() for \_ in range(n)]

maze = [[0] \* m for \_ in range(n)]
maze[n - 1][m - 1] = 1
direction = [1, 0, -1, 0]
bfs(n - 1, m - 1)

print(maze[0][0])</code></pre>
<ul>
<li>(1) 다음 칸을 지나가지 않았거나 지나갔지만 현재가 더 적은 칸을 이동했을 때 큐에 삽입한다.</li>
</ul>