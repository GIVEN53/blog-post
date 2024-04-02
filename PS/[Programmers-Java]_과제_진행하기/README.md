[Programmers-Java] 과제 진행하기
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/176962">https://school.programmers.co.kr/learn/courses/30/lessons/176962</a></p>
<h2>접근</h2>
<ol>
<li>중간에 멈춘 과제는 가장 최근에 멈춘 과제부터 다시 시작하기 때문에 스택에 저장한다.</li>
<li>과제를 시작 시간 순으로 오름차순 정렬한다.</li>
<li>과제를 하나 꺼내서 시작 시간과 소요 시간을 더한 후 다음 과제의 시작 시간과 비교한다.</li>
<li>현재 과제를 다음 과제 시작 전에 마치지 못할 경우 남은 소요 시간을 변경하고 멈춘 과제에 저장한다.</li>
<li>마칠 수 있으면 끝낸 과제에 저장하고 마지막에 멈춘 과제를 꺼낸다.</li>
<li>멈춘 과제를 이어서 진행할 경우 이전 과제를 마친 시간부터 진행한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">import java.util.\*;

class Solution {
 public String[] solution(String[][] plans) {
 LinkedList<Task> tasks = new LinkedList<>();
 for (String[] plan : plans) {
 tasks.offer(new Task(plan[0], convertToMinute(plan[1]), Integer.parseInt(plan[2])));
 }
 tasks.sort((t1, t2) -> t1.start - t2.start); // (1)

 Stack<Task> stopTasks = new Stack<>();
 List<String> endTasks = new ArrayList<>();
 Task now = tasks.poll();
 int time = now.start;
 while (!tasks.isEmpty()) {
 time += now.left;
 Task next = tasks.peek();

 if (time > next.start) { // (2)
 now.left = time - next.start;
 stopTasks.push(now);
 } else { // (3)
 endTasks.add(now.name);
 if (!stopTasks.empty()) { // (4)
 now = stopTasks.pop();
 continue;
 }
 }
 now = tasks.poll();
 time = now.start;
 }

 endTasks.add(now.name); // (5)
 while (!stopTasks.empty()) { // (6)
 endTasks.add(stopTasks.pop().name);
 }

 return endTasks.toArray(new String[0]);
 }

 private int convertToMinute(String time) {
 String[] t = time.split(":");
 return Integer.parseInt(t[0]) \* 60 + Integer.parseInt(t[1]);
 }

 class Task {
 String name;
 int start;
 int left;

 Task(String name, int start, int left) {
 this.name = name;
 this.start = start;
 this.left = left;
 }
 }
}</code></pre>
<ul>
<li>(1) 시작 시간 순으로 정렬한다.</li>
<li>(2) 현재 과제의 마치는 시간이 다음 과제의 시작 시간보다 크면 다음 과제 시작 전까지 과제를 진행한 후 멈춘 과제에 삽입한다.</li>
<li>(3) 작거나 같으면 현재 과제를 마칠 수 있다.</li>
<li>(4) 멈춘 과제가 있으면 한 개 꺼낸다. 멈춘 과제는 현재 시간부터 진행하기 때문에 현재 시간을 변경하지 않는다.</li>
<li>(5) 마지막에 진행된 과제를 끝낸 과제에 삽입한다.</li>
<li>(6) 멈춘 과제가 남아 있으면 마지막에 진행된 과제 이후에 진행한다.</li>
</ul>