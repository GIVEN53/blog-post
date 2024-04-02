[Programmers-Java] 광물 캐기
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/172927">https://school.programmers.co.kr/learn/courses/30/lessons/172927</a></p>
<h2>접근</h2>
<ol>
<li>돌 곡괭이로 광물을 5개씩 캐서 피로도를 구하고 우선순위 큐에 삽입한다.</li>
<li>피로도가 큰 것부터 꺼내면서 다이아몬드 -> 철 -> 돌 곡괭이 순으로 광물을 캔다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">import java.util.\*;

class Solution {
 private static final int[][] PICK\_FATIGUE = {
 { 1, 1, 1 },
 { 5, 1, 1 },
 { 25, 5, 1 }
 }; // (1)

 public int solution(int[] picks, String[] minerals) {
 int pickCnt = Arrays.stream(picks).sum() \* 5;
 if (pickCnt < minerals.length) { // (2)
 minerals = Arrays.copyOfRange(minerals, 0, pickCnt);
 }

 PriorityQueue<int[]> pq = new PriorityQueue<>((o1, o2) -> o2[1] - o1[1]); // (3)
 for (int i = 0; i < minerals.length; i += 5) { // (4)
 int fatigue = 0;
 for (int j = i; j < i + 5 && j < minerals.length; j++) {
 switch (minerals[j]) {
 case "diamond" -> fatigue += PICK\_FATIGUE[2][0];
 case "iron" -> fatigue += PICK\_FATIGUE[2][1];
 case "stone" -> fatigue += PICK\_FATIGUE[2][2];
 }
 }
 pq.offer(new int[] { i, fatigue }); // (5)
 }

 int p = 0;
 for (int i = 0; i < picks.length; i++) {
 if (picks[i] > 0) { // (6)
 p = i;
 break;
 }
 }
 int answer = 0;
 while (!pq.isEmpty()) {
 int m = pq.poll()[0];
 for (int j = m; j < m + 5 && j < minerals.length; j++) { // (7)
 switch (minerals[j]) {
 case "diamond" -> answer += PICK\_FATIGUE[p][0];
 case "iron" -> answer += PICK\_FATIGUE[p][1];
 case "stone" -> answer += PICK\_FATIGUE[p][2];
 }
 }
 if (--picks[p] == 0) { // (8)
 p++;
 }
 }

 return answer;
 }
}</code></pre>
<ul>
<li>(1) 각 곡괭이의 피로도이다.</li>
<li>(2) 광물은 <code>곡괭이 개수의 합 \* 5</code>까지만 캘 수 있기 때문에 캘 수 있는 개수만큼 슬라이싱한다.</li>
<li>(3) 우선순위 큐를 최대 힙으로 초기화한다.</li>
<li>(4) 돌 곡괭이로 광물을 5개씩 캐면서 피로도의 합을 계산한다.</li>
<li>(5) 인덱스와 피로도를 우선순위 큐에 삽입한다. 이 때 피로도를 기준으로 정렬된다.</li>
<li>(6) 다이아몬드, 철, 돌 곡괭이 중 개수가 있는 것을 먼저 선택한다.</li>
<li>(7) 피로도가 큰 순서대로 큐에서 꺼내지면 <code>m</code> 인덱스부터 5개를 캔다.</li>
<li>(8) 곡괭이 개수가 없을 경우 다음 곡괭이를 선택한다.</li>
</ul>