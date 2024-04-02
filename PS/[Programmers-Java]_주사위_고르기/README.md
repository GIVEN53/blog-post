[Programmers-Java] 주사위 고르기
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/258709">https://school.programmers.co.kr/learn/courses/30/lessons/258709</a></p>
<h2>접근</h2>
<ol>
<li>n은 최대 10이다.</li>
<li>n개의 주사위 중 <code>n / 2</code>개를 뽑는 조합 <sub>n</sub>C<sub>n/2</sub> = 252</li>
<li>뽑은 <code>n / 2</code>개의 주사위로 얻을 수 있는 점수의 개수 6<sup>n/2</sup> = 7,776</li>
<li>A와 B의 점수를 비교하여 나올 수 있는 승패 결과의 개수 7,776<sup>2</sup> = 6<sup>n</sup> = 60,466,176</li>
<li><code>252 \* 60,466,176 = 약 152억</code>이기 때문에 시간복잡도를 줄여야 한다.</li>
<li>A가 몇 번 이기는지를 이분 탐색으로 구하면 <code>252 \* 7,776 \* log7,776 = 약 25,474,176</code>으로 시간 내에 해결할 수 있다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">import java.util.\*;

class Solution {
 private int n;
 private List<int[]> diceComb = new ArrayList<>();

 public int[] solution(int[][] dice) {
 this.n = dice.length;
 combineDice(0, 0, new int[n / 2]); // (1)

 int[] answer = {};
 int maxWinCnt = 0;
 for (int[] aComb : diceComb) {
 List<Integer> aScores = new ArrayList<>();
 combineScores(0, 0, aComb, aScores, dice); // (2)
 Collections.sort(aScores);

 int[] bComb = getBComb(aComb);
 List<Integer> bScores = new ArrayList<>();
 combineScores(0, 0, bComb, bScores, dice); // (3)
 Collections.sort(bScores);

 int winCnt = getWinCntOfA(aScores, bScores); // (4)
 if (maxWinCnt < winCnt) {
 maxWinCnt = winCnt;
 answer = aComb;
 }
 }

 for (int i = 0; i < answer.length; i++) {
 answer[i]++; // (5)
 }
 return answer;
 }

 private void combineDice(int start, int cnt, int[] numbers) { 
 if (cnt == n / 2) { // (6)
 diceComb.add(numbers.clone());
 return;
 }

 for (int i = start; i < n; i++) {
 numbers[cnt] = i;
 combineDice(i + 1, cnt + 1, numbers);
 }
 }

 private int[] getBComb(int[] aComb) { // (7)
 boolean[] isA = new boolean[n];
 for (int num : aComb) {
 isA[num] = true; // (8)
 }

 int b = 0;
 int[] bComb = new int[n / 2];
 for (int i = 0; i < n; i++) {
 if (!isA[i]) {
 bComb[b] = i;
 b++;
 }
 }

 return bComb;
 }

 private void combineScores(int cnt, int sum, int[] comb, List<Integer> scores, int[][] dice) {
 if (cnt == n / 2) { // (9)
 scores.add(sum);
 return;
 }

 for (int i = 0; i < 6; i++) {
 combineScores(cnt + 1, sum + dice[comb[cnt]][i], comb, scores, dice);
 }
 }

 private int getWinCntOfA(List<Integer> aScores, List<Integer> bScores) {
 int winCnt = 0;
 for (int s : aScores) { // (10)
 int start = 0;
 int end = bScores.size() - 1;
 while (start <= end) {
 int mid = (start + end) / 2;

 if (s > bScores.get(mid)) {
 start = mid + 1;
 } else {
 end = mid - 1;
 }
 }
 winCnt += start;
 }
 return winCnt;
 }
}</code></pre>
<ul>
<li>(1) <code>n / 2</code>개의 주사위를 선택하는 조합을 구한다.</li>
<li>(2) A의 주사위로 얻을 수 있는 점수를 구한다.</li>
<li>(3) B의 주사위로 얻을 수 있는 점수를 구한다.</li>
<li>(4) A의 몇 번 이기는지 구한다.</li>
<li>(5) 현재 주사위 번호가 0부터 시작하기 때문에 1씩 더해준다.</li>
<li>(6) <code>n / 2</code>개의 주사위를 모두 골랐을 경우 주사위 번호 조합을 리스트에 추가한다.</li>
<li>(7) B가 가져간 나머지 <code>n / 2</code>개의 주사위 번호를 가져온다.</li>
<li>(8) A가 가져간 주사위 번호를 true 처리한다.</li>
<li>(9) <code>n / 2</code>개의 주사위를 모두 굴렸을 경우 나오는 점수를 리스트에 추가한다.</li>
<li>(10) 이분 탐색하여 A의 점수로 이길 수 있는 B의 점수의 개수를 구한다.</li>
</ul>