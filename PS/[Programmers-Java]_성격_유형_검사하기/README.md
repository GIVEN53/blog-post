[Programmers-Java] 성격 유형 검사하기
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/118666">https://school.programmers.co.kr/learn/courses/30/lessons/118666</a></p>
<h2>접근</h2>
<ol>
<li>Map에 성격 유형의 점수를 누적한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">import java.util.\*;

class Solution {
 private static final char[][] MBTI = new char[][] { { 'R', 'T' }, { 'C', 'F' }, { 'J', 'M' }, { 'A', 'N' } }; // (1)
 private Map<Character, Integer> scores = new HashMap<>();

 public String solution(String[] survey, int[] choices) {
 for (int i = 0; i < survey.length; i++) {
 int score = Math.abs(choices[i] - 4);

 if (choices[i] < 4) { // (2)
 increaseScore(survey[i].charAt(0), score);
 } else if (4 < choices[i]) { // (3)
 increaseScore(survey[i].charAt(1), score);
 }
 }

 String answer = "";
 for (char[] m : MBTI) { // (4)
 if (scores.getOrDefault(m[0], 0) >= scores.getOrDefault(m[1], 0)) {
 answer += m[0];
 } else {
 answer += m[1];
 }
 }

 return answer;
 }

 private void increaseScore(char mbti, int score) {
 scores.put(mbti, scores.getOrDefault(mbti, 0) + score);
 }
}</code></pre>
<ul>
<li>(1) 지표 번호 순으로, 각각의 성격 유형을 사전 순으로 선언한다.</li>
<li>(2) 비동의 관련 선택지를 선택하면 첫 번째 성격 유형의 점수가 증가한다.</li>
<li>(3) 동의 관련 선택지를 선택하면 두 번째 성격 유형의 점수가 증가한다.</li>
<li>(4) 성격 유형의 점수를 비교하면서 성격 유형의 문자를 추가한다.</li>
</ul>