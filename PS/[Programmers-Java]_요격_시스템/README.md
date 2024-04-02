[Programmers-Java] 요격 시스템
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/181188">https://school.programmers.co.kr/learn/courses/30/lessons/181188</a></p>
<h2>접근</h2>
<ol>
<li>폭격 미사일을 e를 기준으로 오름차순 정렬한다.</li>
<li>현재 미사일의 s가 이전 미사일의 e보다 크거나 같으면 요격 미사일이 한 개 필요하다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">import java.util.Arrays;

class Solution {
 public int solution(int[][] targets) {
 Arrays.sort(targets, (o1, o2) -> o1[1] - o2[1]); // (1)

 int x = 0;
 int answer = 0;
 for (int[] target : targets) {
 if (x <= target[0]) { // (2)
 x = target[1];
 answer++;
 }
 }
 return answer;
 }
}</code></pre>
<ul>
<li>(1) e를 기준으로 미사일을 오름차순 정렬한다.</li>
<li>(2) 현재 미사일의 s가 x보다 크거나 같으면 x를 현재 미사일의 e로 저장하고 요격 미사일을 한 개 추가한다.</li>
</ul>