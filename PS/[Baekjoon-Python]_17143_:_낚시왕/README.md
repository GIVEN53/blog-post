[Baekjoon-Python] 17143 : 낚시왕
=
<p><a href="https://www.acmicpc.net/problem/17143">https://www.acmicpc.net/problem/17143</a></p>
<h2>접근</h2>
<ol>
<li>격자의 열 크기(C)가 5라면 상어가 이동할 때 인덱스(c)는 <code>0, 1, 2, 3, 4, 3, 2, 1, ...</code>이 된다.</li>
<li>상어가 움직일 때 인덱스에 사이클이 발생한다. 사이클 길이는 <code>2 \* (C - 1)</code>이다.</li>
<li>상어의 이동 후 인덱스를 중복없이 한 번에 찾도록 최적화해야 시간 초과가 발생하지 않는다.</li>
<li>열, 오른쪽 방향 기준으로 상어의 이동 후 인덱스는 <code>(현재 인덱스 + 속력) % 열 사이클 길이</code><br>즉, <code>(c + s) % (2 \* (C - 1))</code>이다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin


def catch(j):
 for i in range(R): # (1)
 if (i, j) in sharks:
 return sharks.pop((i, j))[2] # (2)
 return 0


def move():
 tmp\_sharks = {}
 for (r, c), (s, d, z) in sharks.items():
 nr, nc, d = get\_next\_location(r, c, s, d) # (3)

 if (nr, nc) in tmp\_sharks and tmp\_sharks[(nr, nc)][2] > z: # (4)
 continue
 tmp\_sharks[(nr, nc)] = (s, d, z) # (5)

 return tmp\_sharks


def get\_next\_location(r, c, s, d):
 if d < 2:
 if d == 0: # (6)
 r = r\_cycle - r + s
 else: # (7)
 r += s
 r %= r\_cycle
 if r >= R: # (8)
 return r\_cycle - r, c, 0
 return r, c, 1
 else:
 if d == 3: # (9)
 c = c\_cycle - c + s
 else: # (10)
 c += s
 c %= c\_cycle
 if c >= C: # (11)
 return r, c\_cycle - c, 3
 return c, s, 2


R, C, M = map(int, stdin.readline().split())
sharks = {}
for \_ in range(M):
 r, c, s, d, z = map(int, stdin.readline().split())
 sharks[(r - 1, c - 1)] = (s, d - 1, z)

catch\_size = 0
r\_cycle = 2 \* (R - 1)
c\_cycle = 2 \* (C - 1)
for j in range(C):
 catch\_size += catch(j)
 sharks = move()

print(catch\_size)</code></pre>
<ul>
<li>(1) 열은 낚시왕과 같은 열이고 행만 순회하면서 상어를 찾는다.</li>
<li>(2) 땅과 제일 가까운 상어를 삭제하고 상어의 사이즈를 리턴한다.</li>
<li>(3) 상어가 이동 후 위치를 가져온다.</li>
<li>(4) 이동 후 위치에 다른 상어가 있고 현재 상어보다 사이즈가 크면 현재 상어가 잡아먹히기 때문에 건너뛴다.</li>
<li>(5) 이동 후 위치에 다른 상어가 없거나 다른 상어가 있지만 현재 상어의 사이즈가 더 크면 현재 상어를 저장한다.</li>
<li>(6) 위쪽 방향일 때 <code>r = (r\_cycle - r + s) % r\_cycle</code></li>
<li>(7) 아래쪽 방향일 때 <code>r = (r + s) % r\_cycle</code></li>
<li>(8) 범위를 벗어났을 경우 <code>r = r\_cycle - r</code>이고 방향은 위쪽이 된다.</li>
<li>(9) 왼쪽 방향일 때 <code>c = (c\_cycle - c + s) % c\_cycle</code></li>
<li>(10) 오른쪽 방향일 때 <code>c = (c + s) % c\_cycle</code></li>
<li>(11) 범위를 벗어났을 경우 <code>c = c\_cycle - c</code>이고 방향은 왼쪽이 된다.</li>
</ul>
<h3>예시</h3>
<p>격자의 열 크기(C) = 5, 상어의 인덱스(c) = 2, 속력(s) = 9이라고 가정한다.<br>사이클의 길이는 <code>2 \* (C - 1) = 8</code>이 된다.</p>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/bv72Ai/btsDJkHn9f0/SqwG2tGQWKDFS7bv5go8pk/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/bv72Ai/btsDJkHn9f0/SqwG2tGQWKDFS7bv5go8pk/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fbv72Ai%2FbtsDJkHn9f0%2FSqwG2tGQWKDFS7bv5go8pk%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<h4>오른쪽 방향일 경우</h4>
<ol>
<li><code>c + s = 11</code>이므로 상어는 11번 인덱스에 위치한다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/N9EQu/btsDLIUNIGu/YZNd26mSGbtBwwdhDlDdK0/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/N9EQu/btsDLIUNIGu/YZNd26mSGbtBwwdhDlDdK0/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FN9EQu%2FbtsDLIUNIGu%2FYZNd26mSGbtBwwdhDlDdK0%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<ol start="2">
<li>상어 인덱스를 찾기 위해 사이클 길이로 나눈 나머지를 구한다. <code>11 % 8 = 3</code></li>
</ol>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/cKYEbj/btsDLr6BYLI/wdpevyJ6kwdQ9k3XIwz6J0/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/cKYEbj/btsDLr6BYLI/wdpevyJ6kwdQ9k3XIwz6J0/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcKYEbj%2FbtsDLr6BYLI%2FwdpevyJ6kwdQ9k3XIwz6J0%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<h4>왼쪽 방향일 경우</h4>
<ol>
<li>왼쪽 방향은 상어 인덱스가 <code>4, 3, 2, 1, 0, ...</code>으로 감소한다. 따라서 <code>사이클 길이 - c</code>로 인덱스를 조정한다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/lq8Xd/btsDQ4pbPPl/gctt0Xk2YpD98q8Ha2jko0/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/lq8Xd/btsDQ4pbPPl/gctt0Xk2YpD98q8Ha2jko0/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Flq8Xd%2FbtsDQ4pbPPl%2Fgctt0Xk2YpD98q8Ha2jko0%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<ol start="2">
<li><code>c + s = 15</code>이므로 상어는 15번 인덱스에 위치한다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/AEHHL/btsDQTH1T2Z/pz0uKOyNvhuHqzfblyRyAk/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/AEHHL/btsDQTH1T2Z/pz0uKOyNvhuHqzfblyRyAk/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FAEHHL%2FbtsDQTH1T2Z%2Fpz0uKOyNvhuHqzfblyRyAk%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<ol start="3">
<li>상어 인덱스를 찾기 위해 사이클 길이로 나눈 나머지를 구한다. <code>15 % 8 = 7</code></li>
</ol>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/ctjHQi/btsDQUAdViJ/aMn9tdYy36DlBw6gWpE9B1/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/ctjHQi/btsDQUAdViJ/aMn9tdYy36DlBw6gWpE9B1/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FctjHQi%2FbtsDQUAdViJ%2FaMn9tdYy36DlBw6gWpE9B1%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<ol start="4">
<li>격자 범위 밖이기 때문에 <code>사이클 길이 - c</code>로 인덱스를 조정한다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/bmDaoY/btsDQ6UQphx/d6bilCnY1amjNgLXQEBEkK/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/bmDaoY/btsDQ6UQphx/d6bilCnY1amjNgLXQEBEkK/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbmDaoY%2FbtsDQ6UQphx%2Fd6bilCnY1amjNgLXQEBEkK%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>