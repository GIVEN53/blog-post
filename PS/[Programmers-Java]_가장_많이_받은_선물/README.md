[Programmers-Java] 가장 많이 받은 선물
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/258712">https://school.programmers.co.kr/learn/courses/30/lessons/258712</a></p>
<h2>접근</h2>
<ol>
<li>친구마다 인덱스를 부여한다.</li>
<li>2차원 배열에 선물을 주고 받은 기록을 저장한다.</li>
<li>각각의 선물 지수는 선물을 줄 때 마다 +1, 받을 때마다 -1한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">import java.util.\*;

class Solution {
 public int solution(String[] friends, String[] gifts) {
 int n = friends.length;
 Map<String, Integer> friendIdx = new HashMap<>();
 for (int i = 0; i < n; i++) {
 friendIdx.put(friends[i], i); // (1)
 }

 int[][] giftLog = new int[n][n];
 int[] giftPoint = new int[n];
 for (String gift : gifts) {
 String[] g = gift.split(" ");
 int giver = friendIdx.get(g[0]);
 int taker = friendIdx.get(g[1]);

 giftLog[giver][taker]++; // (2)
 giftPoint[giver]++; // (3)
 giftPoint[taker]--;
 }

 int[] nextMonth = new int[n];
 for (int i = 1; i < n; i++) {
 for (int j = 0; j < i; j++) {
 if (giftLog[i][j] > giftLog[j][i]) { // (4)
 nextMonth[i]++;
 } else if (giftLog[i][j] < giftLog[j][i]) {
 nextMonth[j]++;
 } else { // (5)
 if (giftPoint[i] > giftPoint[j]) {
 nextMonth[i]++;
 } else if (giftPoint[i] < giftPoint[j]) {
 nextMonth[j]++;
 }
 }
 }
 }
 Arrays.sort(nextMonth);
 return nextMonth[n - 1];
 }
}</code></pre>
<ul>
<li>(1) 친구에게 인덱스를 부여한다.</li>
<li>(2) 선물을 주고 받은 기록을 저장한다.</li>
<li>(3) 선물 지수를 계산한다.</li>
<li>(4) i와 j의 선물을 주고 받은 개수를 확인한다.</li>
<li>(5) 선물을 주고 받은 개수가 같으면 선물 지수를 확인한다.</li>
</ul>