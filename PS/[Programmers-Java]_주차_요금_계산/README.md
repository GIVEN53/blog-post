[Programmers-Java] 주차 요금 계산
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/92341">https://school.programmers.co.kr/learn/courses/30/lessons/92341</a></p>
<h2>접근</h2>
<ol>
<li>Map에 주차 시간을 누적한다.</li>
<li>누적된 주차 시간에 따라 주차 요금을 계산한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">import java.util.\*;

class Solution {
 private Map<String, Integer> parkingLot = new HashMap<>();

 public int[] solution(int[] fees, String[] records) {
 for (String record : records) {
 String[] r = record.split(" ");
 int minute = getMinute(r[0]);
 if (r[2].equals("IN")) { // (1)
 minute \*= -1;
 } else {
 minute \*= 1;
 }

 parkingLot.put(r[1], parkingLot.getOrDefault(r[1], 0) + minute);
 }

 for (String carNumber : parkingLot.keySet()) {
 if (parkingLot.get(carNumber) < 1) { // (2)
 parkingLot.put(carNumber, parkingLot.get(carNumber) + 1439);
 }
 }

 String[] carNumbers = parkingLot.keySet().toArray(new String[0]);
 Arrays.sort(carNumbers);

 int[] answer = new int[carNumbers.length];
 for (int i = 0; i < carNumbers.length; i++) {
 int m = parkingLot.get(carNumbers[i]);
 answer[i] = calculateParkingFee(fees, m);
 }
 return answer;
 }

 private int getMinute(String time) {
 String[] t = time.split(":");
 return Integer.parseInt(t[0]) \* 60 + Integer.parseInt(t[1]);
 }

 private int calculateParkingFee(int[] fees, int minute) {
 int fee = fees[1]; // (3)
 minute -= fees[0];

 if (minute > 0) { // (4)
 if (minute % fees[2] == 0) {
 fee += minute / fees[2] \* fees[3];
 } else {
 fee += (minute / fees[2] + 1) \* fees[3];
 }
 }
 return fee;
 }
}</code></pre>
<ul>
<li>(1) <code>IN</code>이면 분을 음수로, <code>OUT</code>이면 분을 양수로 바꿔서 누적한다.</li>
<li>(2) 분이 1보다 작을 경우 출차하지 않은 차기 때문에 <code>23:59</code>를 분으로 변환한 1439를 더한다.</li>
<li>(3) 기본 요금부터 시작하고 기본 시간을 빼준다.</li>
<li>(4) 기본 시간을 초과하면 <code>단위 시간 \* 단위 요금</code>을 더한다.</li>
</ul>