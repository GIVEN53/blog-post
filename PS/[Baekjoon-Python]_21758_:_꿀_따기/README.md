[Baekjoon-Python] 21758 : 꿀 따기
=
<p><a href="https://www.acmicpc.net/problem/21758">https://www.acmicpc.net/problem/21758</a></p>
<h2>접근</h2>
<ol>
<li>꿀의 누적합을 구한다.</li>
<li>벌 또는 벌통은 양 끝에 위치해야 한다.</li>
<li><code>벌, 벌, 벌통</code>, <code>벌, 벌통, 벌</code>, <code>벌통, 벌, 벌</code> 세 가지 경우의 수를 확인하고 최대의 꿀의 양을 구한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin


def fly():
 honey\_amount = 0
 for i in range(1, n - 1):
 # (1)
 bee\_1 = accum\_honey[n - 1] - honey[i] - honey[0] # (2)
 bee\_2 = accum\_honey[n - 1] - accum\_honey[i] # (3)
 honey\_amount = max(honey\_amount, bee\_1 + bee\_2)

 # (4)
 bee\_1 = accum\_honey[i] - honey[0] # (5)
 bee\_2 = accum\_honey[n - 2] - accum\_honey[i - 1] # (6)
 honey\_amount = max(honey\_amount, bee\_1 + bee\_2)

 # (7)
 bee\_1 = accum\_honey[i - 1] # (8)
 bee\_2 = accum\_honey[n - 2] - honey[i] # (9)
 honey\_amount = max(honey\_amount, bee\_1 + bee\_2)
 return honey\_amount


n = int(stdin.readline())
honey = list(map(int, stdin.readline().split()))
accum\_honey = honey[:] 
for i in range(1, n): # (10)
 accum\_honey[i] += accum\_honey[i - 1]

print(fly())</code></pre>
<ul>
<li>(1) <code>벌1 = 0</code>, <code>벌2 = i</code>, <code>벌통 = n - 1</code>이다. <strong>벌2</strong>만 움직이면서 최댓값을 확인한다.</li>
<li>(2) 벌1이 꿀을 딴 양은 <code>꿀 총합 - 벌1 위치의 꿀 양 - 벌2 위치의 꿀 양</code>이다.</li>
<li>(3) 벌2가 꿀을 딴 양은 <code>꿀 총합 - 벌2 위치까지의 꿀 누적합</code>이다.</li>
<li>(4) <code>벌1 = 0</code>, <code>벌통 = i</code>, <code>벌2 = n - 1</code>이다. <strong>벌통</strong>만 움직이면서 최댓값을 확인한다.</li>
<li>(5) 벌1이 꿀을 딴 양은 <code>벌통까지의 꿀 누적합 - 벌1 위치의 꿀 양</code>이다.</li>
<li>(6) 벌2가 꿀을 딴 양은 <code>벌2 위치 전까지의 꿀 누적합 - 벌통 전까지의 꿀 누적합</code>이다.</li>
<li>(7) <code>벌통 = 0</code>, <code>벌1 = i</code>, <code>벌2 = n - 1</code>이다. <strong>벌1</strong>만 움직이면서 최댓값을 확인한다.</li>
<li>(8) 벌1이 꿀을 딴 양은 <code>벌1 위치 전까지의 꿀 누적합</code>이다.</li>
<li>(9) 벌2가 꿀을 딴 양은 <code>벌2 위치 전까지의 꿀 누적합 - 벌1 위치의 꿀 양</code>이다.</li>
<li>(10) 꿀의 누적합을 구한다.</li>
</ul>