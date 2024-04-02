[Baekjoon-Python] 20061 : 모노미노도미노 2
=
<p><a href="https://www.acmicpc.net/problem/20061">https://www.acmicpc.net/problem/20061</a></p>
<h2>접근</h2>
<ol>
<li>새로운 행은 앞에서 추가되고 0, 1행에 블록이 존재할 때 뒤부터 삭제되기 때문에 데큐를 사용한다.</li>
<li>blue는 x를 열로 두고 green과 같이 진행한다.</li>
<li>열이 가득 찬 행을 먼저 삭제하고 0, 1행을 확인한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin
from collections import deque


def find\_top(board, c): # (1)
 for r in range(2, 6): # (2)
 if board[r][c] == 1:
 return r - 1
 return 5


def remove\_full\_col():
 global res
 for board in blue, green:
 for r in range(2, 6):
 if sum(board[r]) == 4: # (3)
 del board[r]
 board.appendleft([0] \* 4)
 res += 1


def execute\_special(): # (4)
 for board in blue, green:
 while 1 in board[1]:
 board.pop()
 board.appendleft([0] \* 4)


n = int(stdin.readline())
blue = deque([[0] \* 4 for \_ in range(6)])
green = deque([[0] \* 4 for \_ in range(6)])
res = 0
for \_ in range(n):
 t, r, c = map(int, stdin.readline().split())
 br, gr = find\_top(blue, r), find\_top(green, c) # (5)
 if t == 2:
 gr = min(gr, find\_top(green, c + 1)) # (6)
 blue[br - 1][r], green[gr][c + 1] = 1, 1
 elif t == 3:
 br = min(br, find\_top(blue, r + 1)) # (7)
 blue[br][r + 1], green[gr - 1][c] = 1, 1
 blue[br][r], green[gr][c] = 1, 1
 remove\_full\_col()
 execute\_special()

print(res)
print(sum(map(sum, blue)) + sum(map(sum, green)))</code></pre>
<ul>
<li>(1) 블록을 놓을 수 있는 행을 찾는다.</li>
<li>(2) 0, 1 행은 항상 블록이 없으므로 제외한다.</li>
<li>(3) 열이 가득 찬 행은 삭제하고 맨 앞에 행을 추가한다.</li>
<li>(4) 0, 1행에 블록이 존재하면 마지막 행부터 삭제한다.</li>
<li>(5) blue는 r을 열로 놓고 찾는다.</li>
<li>(6) green은 1x2 블록이 <code>◻︎◻︎</code> 모양으로 놓이기 때문에 <code>c + 1</code> 열도 확인해서 최소 행을 구한다.</li>
<li>(7) blue는 2x1 블록이 <code>◻︎◻︎</code> 모양으로 놓이기 때문에 <code>r + 1</code> 열도 확인해서 최소 행을 구한다.</li>
</ul>