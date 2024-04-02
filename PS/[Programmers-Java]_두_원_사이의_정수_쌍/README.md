[Programmers-Java] 두 원 사이의 정수 쌍
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/181187">https://school.programmers.co.kr/learn/courses/30/lessons/181187</a></p>
<h2>접근</h2>
<ol>
<li>하나의 사분면에서 점의 개수를 구해서 4를 곱한다.</li>
<li>원의 중심이 (0, 0)이기 때문에 원의 방정식은 x<sup>2</sup> + y<sup>2</sup> = r<sup>2</sup>이다. 따라서 x = (r<sup>2</sup> - y<sup>2</sup>)<sup>1/2</sup>로 x값을 구할 수 있다.</li>
<li>x2의 소수점을 내림, x1의 소수점을 올림하고 <code>x2 - x1 + 1</code> 연산하면 임의의 y 좌표에서 두 원 사이에 있는 정수 x 좌표의 개수가 된다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">class Solution {
 public long solution(int r1, int r2) {
 long answer = 0;
 for (int y = 1; y <= r2; y++) { // (1)
 int x2 = (int) Math.sqrt(Math.pow(r2, 2) - Math.pow(y, 2)); // (2)
 int x1 = (int) Math.ceil(Math.sqrt(Math.pow(r1, 2) - Math.pow(y, 2))); // (3)
 answer += x2 - x1 + 1; // (4)
 }
 return answer \* 4;
 }
}</code></pre>
<ul>
<li>(1) y를 0부터 순회하면 다른 사분면과 중복되는 부분이 발생하기 때문에 1부터 순회한다.</li>
<li>(2) x2를 구한 후 소수점을 내림한다.</li>
<li>(3) x1를 구한 후 소수점을 올림한다.</li>
<li>(4) 점의 개수를 더한다.</li>
</ul>