[Baekjoon-Python] 17142 : 연구소 3
=
<p><a href="https://www.acmicpc.net/problem/17142">https://www.acmicpc.net/problem/17142</a></p>
<h2>접근</h2>
<ol>
<li>바이러스 중 m개의 활성 바이러스를 조합으로 선택한다.</li>
<li>bfs 탐색하면서 바이러스를 퍼뜨린다.</li>
<li>빈 칸의 개수가 0이면 최소 시간을 갱신한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin
from collections import deque
from itertools import combinations


def bfs(virus, empty\_cnt) -> int:
 q = deque(virus)
 visited = [[0] \* n for \_ in range(n)]
 for r, c in virus: # (1)
 visited[r][c] = 1

 while q:
 r, c = q.popleft()

 for i in range(4):
 nr, nc = r + direction[i], c + direction[3 - i]
 if is\_out\_of\_range(nr, nc):
 continue

 if not visited[nr][nc]: # (2)
 if lab[nr][nc] == 0: # (3)
 empty\_cnt -= 1
 visited[nr][nc] = visited[r][c] + 1
 q.append((nr, nc))

 if empty\_cnt == 0: # (4)
 return visited[r][c]

 return n\*\*2 # (5)


def is\_out\_of\_range(r, c):
 return 0 > r or r >= n or 0 > c or c >= n or lab[r][c] == 1


n, m = map(int, stdin.readline().split())
lab = []
virus = []
empty\_cnt = 0
for i in range(n):
 line = list(map(int, stdin.readline().split()))
 lab.append(line)
 for j in range(n):
 if line[j] == 0:
 empty\_cnt += 1
 elif line[j] == 2:
 virus.append((i, j))
if empty\_cnt == 0: # (6)
 print(0)
 exit()

direction = [1, 0, -1, 0]
min\_sec = n\*\*2
for comb in combinations(virus, m): # (7)
 min\_sec = min(min\_sec, bfs(comb, empty\_cnt))

print(min\_sec if min\_sec != n\*\*2 else -1)</code></pre>
<ul>
<li>(1) 활성 바이러스의 r, c 좌표를 1초로 방문 처리한다.</li>
<li>(2) 다음 칸이 방문하지 않은 칸(비활성 바이러스, 빈 칸)일 경우 현재 칸의 방문 시간 + 1로 방문 처리하고 큐에 삽입한다.</li>
<li>(3) 빈 칸일 경우 빈 칸 개수를 감소시킨다.</li>
<li>(4) 바이러스를 모두 퍼뜨렸을 경우 현재 칸의 시간을 리턴한다.</li>
<li>(5) 바이러스를 모두 퍼뜨리지 못했을 경우 최댓값을 리턴한다.</li>
<li>(6) 빈 칸이 없으면 0을 출력하고 종료한다.</li>
<li>(7) 바이러스 중 m개의 활성 바이러스를 조합으로 선택한다.</li>
</ul>