[Programmers-Java] 테이블 해시 함수
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/147354">https://school.programmers.co.kr/learn/courses/30/lessons/147354</a></p>
<h2>접근</h2>
<ol>
<li>튜플을 정렬한다.</li>
<li>i번째 행의 값은 i로 나눈 나머지를 구하고 모두 더한다.</li>
<li>범위 내의 값들을 누적하여 XOR 연산한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">import java.util.Arrays;
import java.util.stream.IntStream;

class Solution {
 public int solution(int[][] data, int col, int row\_begin, int row\_end) {
 int[][] sortedData = sort(data, col - 1); // (1)
 return IntStream.range(row\_begin - 1, row\_end) // (2)
 .map(i -> modAndSum(i + 1, sortedData[i])) // (3)
 .reduce(0, (a, b) -> a ^ b); // (4)
 }

 private int[][] sort(int[][] data, int col) {
 Arrays.sort(data, (o1, o2) -> {
 if (o1[col] == o2[col]) {
 return o2[0] - o1[0];
 }
 return o1[col] - o2[col];
 });
 return data;
 }

 private int modAndSum(int modNum, final int[] data) {
 return Arrays.stream(data)
 .map(d -> d % modNum)
 .sum();
 }
}</code></pre>
<ul>
<li>(1) 튜플을 정렬한다.</li>
<li>(2) <code>row\_begin ~ row\_end</code>의 인덱스만 순회한다.</li>
<li>(3) i로 나눈 나머지의 합을 구한다.</li>
<li>(4) XOR 연산한다.</li>
</ul>