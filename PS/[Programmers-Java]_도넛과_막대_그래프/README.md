[Programmers-Java] 도넛과 막대 그래프
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/258711">https://school.programmers.co.kr/learn/courses/30/lessons/258711</a></p>
<h2>접근</h2>
<ol>
<li><strong>생성한 정점</strong>은 들어오는 간선이 없고 나가는 간선이 2개 이상있다.</li>
<li><strong>도넛</strong>의 모든 정점은 들어오는 간선과 나가는 간선이 1개씩 있다.</li>
<li><strong>막대</strong>의 마지막 정점은 나가는 간선이 없다.</li>
<li><strong>8자</strong>의 정점 중 한 개는 나가는 간선이 2개있다.</li>
<li>생성한 정점과의 간선을 포함하여 특징을 정리하면 다음과 같다.</li>
</ol>
<table>
<thead>
<tr>
<th align="center"></th>
<th>in 간선</th>
<th>out 간선</th>
</tr>
</thead>
<tbody><tr>
<td align="center">생성한 정점</td>
<td>0</td>
<td>> 1</td>
</tr>
<tr>
<td align="center">도넛 (모든 정점)</td>
<td>>= 1</td>
<td>1</td>
</tr>
<tr>
<td align="center">막대 (마지막 정점)</td>
<td>>= 1</td>
<td>0</td>
</tr>
<tr>
<td align="center">8자 (한 정점)</td>
<td>>= 2</td>
<td>2</td>
</tr>
</tbody></table>
<h2>풀이</h2>
<pre><code class="java">import java.util.\*;

class Solution {
 public int[] solution(int[][] edges) {
 Map<Integer, Integer> out = new HashMap<>();
 Map<Integer, Integer> in = new HashMap<>();
 int[] answer = new int[4];

 for (int[] edge : edges) { // (1)
 out.put(edge[0], out.getOrDefault(edge[0], 0) + 1);
 in.put(edge[1], in.getOrDefault(edge[1], 0) + 1);
 }

 for (int node : out.keySet()) {
 if (out.get(node) > 1) { // (2)
 if (!in.containsKey(node)) {
 answer[0] = node;
 } else {
 answer[3] += 1;
 }
 }
 }

 for (int node : in.keySet()) {
 if (!out.containsKey(node)) { // (3)
 answer[2] += 1;
 }
 }
 answer[1] = out.get(answer[0]) - answer[2] - answer[3]; // (4)
 return answer;
 }
}</code></pre>
<ul>
<li>(1) a -> b 간선이라면 in에 b를, out에 a를 저장한다.</li>
<li>(2) out 간선 개수가 2개 이상인 정점 중에서 in 간선이 없으면 생성한 정점이고, 있으면 8자 그래프이다.</li>
<li>(3) in 간선이 있는 정점 중에서 out 간선이 없으면 막대 그래프이다.</li>
<li>(4) 도넛 그래프 개수는 <code>생성한 정점의 out 간선 개수 - 막대 그래프 개수 - 8자 그래프 개수</code>이다.</li>
</ul>