[Programmers-Java] 석유 시추
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/250136">https://school.programmers.co.kr/learn/courses/30/lessons/250136</a></p>
<h2>접근</h2>
<ol>
<li>석유를 bfs 탐색해서 덩어리마다 숫자로 라벨링한다.</li>
<li>Map에 덩어리의 석유량을 저장한다.</li>
<li>열마다 시추관을 설치하고 만날 수 있는 덩어리의 숫자를 저장한다.</li>
<li>덩어리의 석유량을 합한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">import java.util.\*;

class Solution {
 private int n;
 private int m;
 private Map<Integer, Integer> oilAmount = new HashMap<>();
 private int[] directions = new int[] {1, 0, -1, 0};

 public int solution(int[][] land) {
 this.n = land.length;
 this.m = land[0].length;

 int num = 2;
 for (int i = 0; i < n; i++) {
 for (int j = 0; j < m; j++) {
 if (land[i][j] == 1) {
 bfs(i, j, land, num); // (1)
 num++;
 }
 }
 }

 int[] result = new int[m];
 for (int j = 0; j < m; j++) { // (2)
 Set<Integer> oilGroup = new HashSet<>();
 for (int i = 0; i < n; i++) { // (3)
 if (land[i][j] > 1) {
 oilGroup.add(land[i][j]);
 }
 }

 for (int groupNumber : oilGroup) { // (4)
 result[j] += oilAmount.get(groupNumber);
 }
 }

 Arrays.sort(result);
 return result[result.length - 1];
 }

 private void bfs(int i, int j, int[][] land, int groupNumber) {
 Queue<Node> q = new LinkedList<>();
 q.offer(new Node(i, j));
 land[i][j] = groupNumber;
 int amount = 1;
 while (!q.isEmpty()) {
 Node now = q.poll();

 for (int d = 0; d < 4; d++) {
 int ni = now.i + directions[d];
 int nj = now.j + directions[3 - d];

 if (!isOutOfRange(ni, nj) && land[ni][nj] == 1) {
 land[ni][nj] = groupNumber;
 q.offer(new Node(ni, nj));
 amount++;
 }
 }
 }
 oilAmount.put(groupNumber, amount);
 }

 private boolean isOutOfRange(int i, int j) {
 return i < 0 || i >= n || j < 0 || j >= m;
 }

 class Node {
 int i;
 int j;

 Node(int i, int j) {
 this.i = i;
 this.j = j;
 }
 }
}</code></pre>
<ul>
<li>(1) 석유 덩어리를 bfs 탐색한다. land 배열은 0, 1로 이루어져 있기 때문에 2부터 시작해서 석유 덩어리에 숫자를 라벨링한다.</li>
<li>(2) 시추관을 설치할 열을 순회한다.</li>
<li>(3) 행을 순회하면서 라벨링한 숫자를 저장한다. 중복된 숫자를 제거하기 위해 Set을 사용한다.</li>
<li>(4) 석유 덩어리의 크기를 더한다.</li>
</ul>