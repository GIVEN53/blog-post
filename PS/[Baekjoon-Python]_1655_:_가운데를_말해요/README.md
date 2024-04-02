[Baekjoon-Python] 1655 : 가운데를 말해요
=
<p><a href="https://www.acmicpc.net/problem/1655">https://www.acmicpc.net/problem/1655</a></p>
<h2>접근</h2>
<ol>
<li>최대 힙과 최소 힙 두 개를 사용한다.</li>
<li>최대 힙 길이와 최소 힙 길이가 같으면 최대 힙에 삽입하고, 길이가 다르면 최소 힙에 삽입한다.</li>
<li>최대 힙의 최댓값을 최소 힙의 최솟값보다 작게 만든다.</li>
<li>최대 힙의 0번 인덱스 값이 중간 값이다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin
from heapq import heappush, heappop


max\_heap = []
min\_heap = []
for \_ in range(int(stdin.readline())):
 x = int(stdin.readline())

 if len(max\_heap) == len(min\_heap): # (1)
 heappush(max\_heap, x \* -1)
 else: # (2)
 heappush(min\_heap, x)

 if len(max\_heap) > 0 and len(min\_heap) > 0 and max\_heap[0] \* -1 > min\_heap[0]: # (3)
 mx = heappop(max\_heap) \* -1
 mn = heappop(min\_heap)

 heappush(max\_heap, mn \* -1)
 heappush(min\_heap, mx)

 print(max\_heap[0] \* -1) # (4)</code></pre>
<ul>
<li>(1) 두 힙의 길이가 같으면 정수를 최대 힙에 삽입한다.</li>
<li>(2) 길이가 다르면 정수를 최소 힙에 삽입한다.</li>
<li>(3) 최대 힙의 최댓값이 최소 힙의 최솟값보다 크면 두 값의 힙 위치를 교체한다.</li>
<li>(4) 최대 힙의 0번 인덱스 값이 중간 값이 된다.</li>
</ul>