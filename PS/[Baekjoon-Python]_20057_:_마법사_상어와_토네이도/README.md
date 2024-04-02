[Baekjoon-Python] 20057 : 마법사 상어와 토네이도
=
<p><a href="https://www.acmicpc.net/problem/20057">https://www.acmicpc.net/problem/20057</a></p>
<h2>접근</h2>
<ol>
<li>비율이 적힌 칸의 인덱스를 미리 계산한다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/ccHaTk/btsDQU1RdgK/KCGXCeJ7xA8BTZqpvvyjmK/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/ccHaTk/btsDQU1RdgK/KCGXCeJ7xA8BTZqpvvyjmK/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FccHaTk%2FbtsDQU1RdgK%2FKCGXCeJ7xA8BTZqpvvyjmK%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<ol start="2">
<li>토네이도는 x번 전진을 두 번하면 x + 1번 전진한다.</li>
<li>y의 모래를 비율이 적힌 칸으로 모두 이동시킨 후에 남은 모래를 알파로 이동시킨다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin
from math import floor


def tornado(r, c, d):
 over\_amount = 0
 sand, board[r][c] = board[r][c], 0
 dr, dc = direction[d]
 tmp = 0
 for i in range(9): # (1)
 pr, pc = p\_direction[d][i]
 moved\_sand = floor(sand \* percent[i])
 if is\_out\_of\_range(r + pr, c + pc): # (2)
 over\_amount += moved\_sand
 else:
 board[r + pr][c + pc] += moved\_sand
 tmp += moved\_sand

 sand -= tmp # (3)
 if is\_out\_of\_range(r + dr, c + dc):
 over\_amount += sand
 else:
 board[r + dr][c + dc] += sand

 return over\_amount


def is\_out\_of\_range(r, c):
 return r < 0 or r >= n or c < 0 or c >= n


n = int(stdin.readline())
board = [list(map(int, stdin.readline().split())) for \_ in range(n)]

direction = [(0, -1), (1, 0), (0, 1), (-1, 0)]
percent = [0.01, 0.07, 0.02, 0.1, 0.05, 0.1, 0.07, 0.02, 0.01]
p\_direction = [
 [(-1, 1), (-1, 0), (-2, 0), (-1, -1), (0, -2), (1, -1), (1, 0), (2, 0), (1, 1)],
 [(-1, -1), (0, -1), (0, -2), (1, -1), (2, 0), (1, 1), (0, 1), (0, 2), (-1, 1)],
 [(1, -1), (1, 0), (2, 0), (1, 1), (0, 2), (-1, 1), (-1, 0), (-2, 0), (-1, -1)],
 [(1, 1), (0, 1), (0, 2), (-1, 1), (-2, 0), (-1, -1), (0, -1), (0, -2), (1, -1)],
] # (4)
moved = [0] \* n
d, cnt = 0, 1
r = c = n // 2 # (5)
res = 0
while r != 0 or c != 0:
 if moved[cnt] == 2 and cnt < n - 1: # (6)
 cnt += 1

 for \_ in range(cnt):
 r += direction[d][0]
 c += direction[d][1]
 res += tornado(r, c, d)

 d = (d + 1) % 4
 moved[cnt] += 1

print(res)</code></pre>
<ul>
<li>(1) 모래 비율을 순회한다.</li>
<li>(2) 격자 밖으로 나간 모래의 양을 더한다.</li>
<li>(3) 알파에 해당하는 모래의 양이다.</li>
<li>(4) 이동 방향에 따라 y를 기준으로 모래 비율이 적힌 칸의 인덱스를 의미한다.<br> 방향은 <code>0:좌, 1: 하, 2:우, 3:상</code>이다.</li>
<li>(5) 격자의 정중앙 인덱스로 초기화한다.</li>
<li>(6) cnt는 전진 횟수이다. 토네이도는 x번 전진을 두 번 하면 다음은 x + 1번 전진을 두 번한다. 마지막 토네이도의 전진만 세 번하기 때문에 <code>cnt < n - 1</code> 조건을 추가한다.<br><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/ZSuWc/btsDJZwxs74/e83tvMNCbKl3Wip3CLJGz0/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/ZSuWc/btsDJZwxs74/e83tvMNCbKl3Wip3CLJGz0/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FZSuWc%2FbtsDJZwxs74%2Fe83tvMNCbKl3Wip3CLJGz0%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</li>
</ul>