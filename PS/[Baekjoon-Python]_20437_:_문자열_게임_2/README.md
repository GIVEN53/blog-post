[Baekjoon-Python] 20437 : 문자열 게임 2
=
<p><a href="https://www.acmicpc.net/problem/20437">https://www.acmicpc.net/problem/20437</a></p>
<h2>접근</h2>
<ol>
<li>알파벳의 <code>ASCII - 97</code>을 인덱스로 사용한다.</li>
<li>알파벳마다 문자열의 인덱스를 저장한다.</li>
<li>알파벳을 순회하면서 k개 포함하는 인덱스 2개를 찾고, 문자열의 길이를 구한다.</li>
<li>최소 길이, 최대 길이를 갱신한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin


def play():
 min\_len, max\_len = 1e9, 0
 for alpha in alphabet:
 if len(alpha) < k: # (1)
 continue
 for i in range(len(alpha) - k + 1): 
 length = alpha[i + k - 1] - alpha[i] + 1 # (2)
 if length < min\_len:
 min\_len = length
 if length > max\_len:
 max\_len = length
 if max\_len == 0: # (3)
 print(-1)
 else:
 print(min\_len, max\_len)


t = int(stdin.readline())
for \_ in range(t):
 w, k = stdin.readline().rstrip(), int(stdin.readline())
 alphabet = [[] for \_ in range(26)] # (4)
 for j, word in enumerate(w):
 i = ord(word) - 97
 alphabet[i].append(j)
 play()</code></pre>
<ul>
<li>(1) k개보다 적은 알파벳은 건너뛴다.</li>
<li>(2) 해당 알파벳이 k개 포함하는 문자열 길이를 구한다.</li>
<li>(3) 알파벳이 전부 k보다 개수가 적을 경우 최대 길이 또는 최소 길이는 갱신되지 않는다.</li>
<li>(4) <code>a: 0 ~ z: 25</code>로 인덱스를 지정하고 알파벳마다 문자열의 인덱스를 저장한다.</li>
</ul>